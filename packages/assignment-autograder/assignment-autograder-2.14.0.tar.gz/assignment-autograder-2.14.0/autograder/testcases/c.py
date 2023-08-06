from pathlib import Path

import sh

from .abstract_base_class import ArgList, Command, ShCommand, TestCase


class CTestCase(TestCase):
    source_suffix = ".c"
    executable_suffix = ".out"
    helper_module_name = "test_helper.c"
    SUBMISSION_COMPILATION_ARGS = ("-Dscanf_s=scanf", "-Dmain=__student_main__")
    compiler = Command("gcc")

    @classmethod
    def is_installed(cls) -> bool:
        return cls.compiler is not None

    @classmethod
    def precompile_submission(
        cls,
        submission: Path,
        student_dir: Path,
        possible_source_file_stems: str,
        source_is_case_insensitive: bool,
        arglist,
    ):
        """Links student submission without compiling it.
        It is done to speed up total compilation time
        """
        copied_submission = super().precompile_submission(
            submission, student_dir, [submission.stem], source_is_case_insensitive, arglist
        )
        precompiled_submission = copied_submission.with_suffix(".o")
        try:
            cls.compiler(
                "-c",
                f"{copied_submission}",
                "-o",
                precompiled_submission,
                *cls.SUBMISSION_COMPILATION_ARGS,
                *arglist,
            )
        finally:
            copied_submission.unlink()
        return precompiled_submission

    def precompile_testcase(self):
        self.compiler(
            "-c",
            self.path,
            "-o",
            self.path.with_suffix(".o"),
            *self.argument_lists[ArgList.TESTCASE_PRECOMPILATION],
        )
        self.path.unlink()
        self.path = self.path.with_suffix(".o")

    def compile_testcase(self, precompiled_submission: Path) -> ShCommand:
        executable_path = self.make_executable_path(precompiled_submission)
        self.compiler(
            "-o",
            executable_path,
            precompiled_submission.with_name(self.path.name),
            str(precompiled_submission),
            *self.argument_lists[ArgList.TESTCASE_COMPILATION],
        )
        return sh.Command(executable_path)
