FILENAME_RUN = "Main"


commands = {
    ".py": {
        "image": "python:3",
        "run": ["/bin/bash", "-c",
                f"python {FILENAME_RUN}.py"],
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
