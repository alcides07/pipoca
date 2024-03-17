from constants import FILENAME_RUN, INPUT_TEST_FILENAME, OUTPUT_JUDGE_FILENAME, OUTPUT_USER_FILENAME

commands = {
    "python.3": {
        "image": "python:3",
        "extension": ".py",
        "run_test": [
            "/bin/bash", "-c",
            f"python3 {FILENAME_RUN}.py < {INPUT_TEST_FILENAME}"
        ],
        "run_checker": [
            "/bin/bash", "-c",
            f"python3 {FILENAME_RUN}.py && ./{FILENAME_RUN} {INPUT_TEST_FILENAME} {OUTPUT_USER_FILENAME} {OUTPUT_JUDGE_FILENAME}"
        ],
        "run_gerador": [
            "/bin/bash", "-c",
            f"python3 {FILENAME_RUN}.py && ./{FILENAME_RUN} $(cat {INPUT_TEST_FILENAME})"
        ]
    },

    "java11": {
        "image": "openjdk:11",
        "extension": ".java",
        "run_test": [
            "/bin/bash", "-c",
            f"javac {FILENAME_RUN}.java && java {FILENAME_RUN} < {INPUT_TEST_FILENAME}"
        ],
        "run_checker": [
            "/bin/bash", "-c",
            f"javac {FILENAME_RUN}.java && java {FILENAME_RUN} && ./{FILENAME_RUN} {INPUT_TEST_FILENAME} {OUTPUT_USER_FILENAME} {OUTPUT_JUDGE_FILENAME}"
        ],
        "run_gerador": [
            "/bin/bash", "-c",
            f"javac {FILENAME_RUN}.java && java {FILENAME_RUN} && ./{FILENAME_RUN} $(cat {INPUT_TEST_FILENAME})"
        ]
    },

    "ruby.3": {
        "image": "ruby:3",
        "extension": ".rb",
        "run_test": [
            "/bin/bash", "-c",
            f"ruby {FILENAME_RUN}.rb < {INPUT_TEST_FILENAME}"
        ],
        "run_checker": [
            "/bin/bash", "-c",
            f"ruby {FILENAME_RUN}.rb && ./{FILENAME_RUN} {INPUT_TEST_FILENAME} {OUTPUT_USER_FILENAME} {OUTPUT_JUDGE_FILENAME}"
        ],
        "run_gerador": [
            "/bin/bash", "-c",
            f"ruby {FILENAME_RUN}.rb && ./{FILENAME_RUN} $(cat {INPUT_TEST_FILENAME})"
        ]
    },

    "cpp.g++17": {
        "image": "gcc",
        "extension": ".cpp",
        "run_test": [
            "/bin/bash", "-c",
            f"g++ -std=c++17 -o {FILENAME_RUN} {FILENAME_RUN}.cpp && ./{FILENAME_RUN} < {INPUT_TEST_FILENAME}"
        ],
        "run_checker": [
            "/bin/bash", "-c",
            f"g++ -std=c++17 -o {FILENAME_RUN} {FILENAME_RUN}.cpp && ./{FILENAME_RUN} {INPUT_TEST_FILENAME} {OUTPUT_USER_FILENAME} {OUTPUT_JUDGE_FILENAME}"
        ],
        "run_gerador": [
            "/bin/bash", "-c",
            f"g++ -std=c++17 -o {FILENAME_RUN} {FILENAME_RUN}.cpp && ./{FILENAME_RUN} $(cat {INPUT_TEST_FILENAME})"
        ]
    }
}
