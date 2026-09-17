name: TEST - Kokoro Audio

on:
  workflow_dispatch:

jobs:
  test-kokoro:
    runs-on: ubuntu-latest

    steps:
      # ============================================================
      # 1. CHECKOUT
      # ============================================================
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          lfs: true
          fetch-depth: 1

      # ============================================================
      # 2. PYTHON
      # ============================================================
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      # ============================================================
      # 3. INSTALL DEPENDENCIES
      # ============================================================
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip

          pip install \
            kokoro-onnx \
            soundfile \
            numpy

      # ============================================================
      # 4. CHECK KOKORO FILES
      # ============================================================
      - name: Check Kokoro model files
        run: |
          echo "============================================================"
          echo "KOKORO MODEL FILE CHECK"
          echo "============================================================"

          MODEL="02_英语学习系统/models/kokoro/kokoro-v1.1-zh.fp16.onnx"
          VOICES="02_英语学习系统/models/kokoro/voices-v1.1-zh.bin"

          echo
          echo "MODEL:"
          ls -lh "$MODEL"

          echo
          echo "VOICES:"
          ls -lh "$VOICES"

          echo
          echo "MODEL SIZE:"
          wc -c "$MODEL"

          echo
          echo "VOICES SIZE:"
          wc -c "$VOICES"

          echo
          echo "GIT LFS:"
          git lfs ls-files || true

          echo
          echo "MODEL HEADER:"
          head -c 200 "$MODEL" | strings || true

      # ============================================================
      # 5. RUN STANDALONE TEST
      # ============================================================
      - name: Run Kokoro standalone test
        run: |
          python 02_英语学习系统/scripts/test_kokoro.py

      # ============================================================
      # 6. SHOW OUTPUT
      # ============================================================
      - name: Check generated audio
        if: always()
        run: |
          echo "============================================================"
          echo "GENERATED AUDIO"
          echo "============================================================"

          ls -lah \
            02_英语学习系统/output/kokoro_test/ \
            || true

      # ============================================================
      # 7. UPLOAD TEST AUDIO
      # ============================================================
      - name: Upload test audio
        if: success()
        uses: actions/upload-artifact@v4
        with:
          name: kokoro-test-audio
          path: 02_英语学习系统/output/kokoro_test/kokoro_test.mp3
          if-no-files-found: error
