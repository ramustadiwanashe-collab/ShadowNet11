from app import simulate_command

def test_pwd():
    assert simulate_command("pwd") == "/home/student"

def test_echo():
    assert simulate_command("echo hello world") == "hello world"

def test_unknown_command_is_not_executed():
    assert "command not found" in simulate_command("rm -rf /")
