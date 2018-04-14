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
    newest_follower_id = get_last_newest_follower_id()

    while True:
        print(f"newest_follower_id: {newest_follower_id}")
        try:
            next_cursor, previous_cursor, followers = api.GetFollowersPaged(
                cursor=newest_follower_id,
                count=config.BTZ_GET_FOLLOWERS_PAGINATION,
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
            for i, follower in enumerate(followers):
                pprint(follower._json)
                if i == 0:
                    newest_follower_id = follower.id
        finally:
            if newest_follower_id is not None:
                save_newest_follower_id(newest_follower_id)

        time.sleep(config.BTZ_CHECK_INTERVAL_SECONDS)

if __name__ == "__main__":
    main()
