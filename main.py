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


def main():
    last_newest_follower_id = get_last_newest_follower_id()

    next_cursor = None
    first_round = True
    while True:
        try:
            next_cursor, previous_cursor, followers = api.GetFollowersPaged(
                cursor=next_cursor or last_newest_follower_id or -1,
                count=config.BTZ_GET_FOLLOWERS_PAGINATION_SIZE,
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

            if first_round:
                last_newest_follower_id = previous_cursor
                first_round = False

            for follower in followers:
                pprint(follower._json)

        finally:
            if last_newest_follower_id is not None:
                save_newest_follower_id(last_newest_follower_id)

        if next_cursor == 0:
            time.sleep(config.BTZ_CHECK_INTERVAL_SECONDS)
            first_round = True
            next_cursor = None

if __name__ == "__main__":
    main()
