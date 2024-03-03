FILENAME_RUN = "Main"
INPUT_FILENAME = "input.txt"

commands = {
    ".py": {
        "image": "python:3",
        "run": ["/bin/bash", "-c",
                f"python {FILENAME_RUN}.py < {INPUT_FILENAME}"],
    },

    ".java": {
        "image": "openjdk:11",
        "run": [
            "/bin/bash", "-c",
            f"javac {FILENAME_RUN}.java && java {FILENAME_RUN}"
        ]
    },

    ".rb": {
        "image": "ruby:3",
        "run": [
            "/bin/bash", "-c",
            f"ruby {FILENAME_RUN}.rb"
        ]
    }
}
