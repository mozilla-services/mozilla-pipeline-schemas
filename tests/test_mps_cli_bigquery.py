def test_main(tmp_git):
    # choose a base ref relative to HEAD, since the head ref may be master
    main(["--root-directory", str(tmp_git), "--base-ref", "HEAD~1"])
    assert len(os.listdir(tmp_git / "integration")) == 3


def test_main_duplicate(tmp_git):
    main(["--root-directory", str(tmp_git), "--base-ref", "HEAD", "--head-ref", "HEAD"])
    assert len(os.listdir(tmp_git / "integration")) == 2
    assert (
        not next((tmp_git / "integration").glob("*.diff")).open().read()
    ), "diff should be empty"
