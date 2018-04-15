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


def get_last_round_newest_follower_id():
    try:
        with open(config.BTZ_LAST_ROUND_NEWEST_FOLLOWER_ID_FILENAME, 'r') as f:
            return int(f.read())
    except:
        return None


def save_newest_follower_id(newest_follower_id):
    with open(config.BTZ_LAST_ROUND_NEWEST_FOLLOWER_ID_FILENAME, 'w') as f:
        f.write(str(newest_follower_id))


def log_blocked_user(blocked_user):
    with open(config.BTZ_BLOCKED_USERS_LOG_FILENAME, 'a') as f:
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"[{now}] @{blocked_user.screen_name} {blocked_user.id}\n")

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
            log_blocked_user(follower)
            print(f"Blocked user: @{follower.screen_name}")


def main():
    newest_follower_id = get_last_round_newest_follower_id()
    print(f"newest_follower_id: {newest_follower_id}")

    next_cursor = None
    first_round = True
    break_at_newest_follower = False
    while True:
        try:
            next_cursor, previous_cursor, followers = api.GetFollowersPaged(
                cursor=next_cursor,
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
                if follower.id == newest_follower_id:
                    print(f"Break at newest_follower_id: {newest_follower_id}, @{follower.screen_name}")
                    break_at_newest_follower = True
                    break

                if first_round:
                    newest_follower_id = follower.id
                    first_round = False

                # pprint(follower._json)
                block_if_zombie(follower)

        finally:
            if newest_follower_id is not None:
                save_newest_follower_id(newest_follower_id)

        if break_at_newest_follower or next_cursor == 0:
            time.sleep(config.BTZ_CHECK_INTERVAL_SECONDS)
            next_cursor = None
            first_round = True
            break_at_newest_follower = False

if __name__ == "__main__":
    main()
