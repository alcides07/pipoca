FILENAME_RUN = "Main"
INPUT_TEST_FILENAME = "input.txt"
OUTPUT_JUDGE_FILENAME = "output_judge.txt"
OUTPUT_USER_FILENAME = "output_user.txt"

commands = {
    ".py": {
        "image": "python:3",
        "extension": ".py",
        "run": ["/bin/bash", "-c",
                f"python {FILENAME_RUN}.py < {INPUT_TEST_FILENAME}"],
    },

    ".java": {
        "image": "openjdk:11",
        "extension": ".java",
        "run": [
            "/bin/bash", "-c",
            f"javac {FILENAME_RUN}.java && java {FILENAME_RUN} < {INPUT_TEST_FILENAME}"
        ]
    },

    ".rb": {
        "image": "ruby:3",
        "extension": ".rb",
        "run": [
            "/bin/bash", "-c",
            f"ruby {FILENAME_RUN}.rb"
        ]
    },

    ".cpp": {
        "image": "gcc",
        "extension": ".cpp",
        "run": [
            "/bin/bash", "-c",
            f"g++ -o {FILENAME_RUN} {FILENAME_RUN}.cpp && ./{FILENAME_RUN} < {INPUT_TEST_FILENAME}"
        ]
    },

    "cpp.g++17": {
        "image": "gcc",
        "extension": ".cpp",
        "run": [
            "/bin/bash", "-c",
            f"g++ -std=c++17 -o {FILENAME_RUN} {FILENAME_RUN}.cpp && ./{FILENAME_RUN} {INPUT_TEST_FILENAME} {OUTPUT_USER_FILENAME} {OUTPUT_JUDGE_FILENAME}"
        ]
    }
}
