import pytest

from app.User.dao import UserDAO

@pytest.mark.parametrize(
    "username,is_present",
    [
        ("alice",True),
        ("bob",True),
        ("sdsadad",False)
    ],
)
async def test_find_one_or_none_user(username,is_present):
    user = await UserDAO.find_one_or_none(username = username)
    if is_present:
        assert user
        assert user.username == username
    else:
        assert not user
        
@pytest.mark.parametrize(
    "user_id,username,email,is_present",
    [
        (1,"alice","alice@example.com", True),
        (2,"bob","bob@example.com", True),
        (3,"charlie","charlie@example.com", True),
        (5, "ss","....", False),
    ],
)
async def test_find_user_by_id(user_id,username,email,is_present):
    user = await UserDAO.find_by_id(user_id)
    if is_present:
        assert user
        assert user.id == user_id
        assert user.email == email
        assert user.username == username
    else:
        assert user.username != username