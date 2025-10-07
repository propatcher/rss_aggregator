import pytest

from app.User.auth import get_password_hash
from app.User.dao import UserDAO

@pytest.mark.parametrize(
    "username,email,password,is_present",
    [
        ("Test","Test@email.com","Secret1",True),
        ("Example","Example@email.com","Secret2",True),
    ],
)
async def test_add_user(username,email,password,is_present):
    hashed_password = get_password_hash(password)
    user = await UserDAO.add(
        username=username,
        email=email,
        hashed_password=hashed_password,
    )
    if is_present:
        assert user
        assert user.username == username
    else:
        assert not user

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