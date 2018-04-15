import datetime
import time
from pprint import pprint

import twitter

import config


api = twitter.Api(
    consumer_key=config.TWITTER_CONSUMER_KEY,
    consumer_secret=config.TWITTER_CONSUMER_SECRET,
    access_token_key=config.TWITTER_ACCESS_TOKEN_KEY,
    access_token_secret=config.TWITTER_ACCESS_TOKEN_SECRET,
)


def get_last_newest_follower_id():
    try:
        with open(config.BTZ_LAST_NEWEST_FOLLOWER_ID_FILENAME, 'r') as f:
            return int(f.read())
    except:
        return None


def save_newest_follower_id(newest_follower_id):
    with open(config.BTZ_LAST_NEWEST_FOLLOWER_ID_FILENAME, 'w') as f:
        f.write(str(newest_follower_id))


def log_blocked_user(blocked_user):
    with open(config.BTZ_BLOCKED_USERS_LOG_FILENAME, 'a') as f:
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"[{now}] @{blocked_user.screen_name} {blocked_user.id}")

def block_if_zombie(follower):
    # Zombie: No followers and use default profile image.
    if (
        follower.followers_count <= 1 and
        "http://abs.twimg.com/sticky/default_profile_images" in follower.profile_image_url and
        follower.statuses_count == 0
    ):
        try:
            api.CreateBlock(
                user_id=follower.id,
                include_entities=False,
                skip_status=True,
            )
        except Exception as e:
            print(e)
            print(f"Failed to blocked user: @{blocked_user.screen_name}")
        else:
            print(f"Blocked user: @{blocked_user.screen_name}")
            log_blocked_user(follower)


def main():
    last_newest_follower_id = get_last_newest_follower_id()

    next_cursor = None
    first_round = True
    while True:
        try:
            next_cursor, previous_cursor, followers = api.GetFollowersPaged(
                cursor=next_cursor or last_newest_follower_id or -1,
                skip_status=True,
                include_user_entities=False,
            )

        except twitter.error.TwitterError as e:
            print(e)

        except KeyboardInterrupt:
            return

        else:
            print(f"next_cursor: {next_cursor}")
            print(f"previous_cursor: {previous_cursor}")

            for follower in followers:
                if first_round:
                    last_newest_follower_id = follower.id
                    first_round = False

                pprint(follower._json)
                block_if_zombie(follower)

        finally:
            if last_newest_follower_id is not None:
                save_newest_follower_id(last_newest_follower_id)

        if next_cursor == 0:
            time.sleep(config.BTZ_CHECK_INTERVAL_SECONDS)
            first_round = True
            next_cursor = None

if __name__ == "__main__":
    main()
