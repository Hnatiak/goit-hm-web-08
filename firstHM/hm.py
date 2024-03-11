from typing import List, Any
import re
import redis
from redis_lru import RedisLRU
from models import Author, Quote

client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)

@cache
def find_by_tag(tag: str) -> list[str | None]:
    print(f'find by {tag}')
    quotes = Quote.objects(tags__iregex=tag)
    result = [q.quote for q in quotes]
    return result

@cache
def find_by_author(author: str) -> list[list[Any]]:
    print(f'find by {author}')
    authors = Author.objects(fullname__iregex=author)
    # result = []
    result = {}
    for a in authors:
        quotes = Quote.objects(author=a)
        # result.append([q.quote for q in quotes])
        result[a.fullname] = [q.quote for q in quotes]
    return result

def find_by_tags(tags: str) -> list[str | None]:
    print(f'Finding by tags: {tags}')
    tag_list = tags.split(',')
    quotes = Quote.objects(tags__all=[re.compile(tag, re.IGNORECASE) for tag in tag_list])
    result = [q.quote for q in quotes]
    return result

if __name__ == '__main__':
    while True:
        command = input("Enter command (name: author_name, tag: tag_name, tags: tag1,tag2,..., exit to quit): ")
        if command.lower() == 'exit':
            break
        elif command.startswith('name:'):
            author_name = command.split(':')[1].strip()
            result = find_by_author(author_name)
            for author, quotes in result.items():
                print(f"Quotes by {author}:")
                for quote in quotes:
                    print(f"- {quote}")
        elif command.startswith('tag:'):
            tag_name = command.split(':')[1].strip()
            result = find_by_tag(tag_name)
            print("Quotes with tag:")
            for quote in result:
                print(f"- {quote}")
        elif command.startswith('tags:'):
            tags = command.split(':')[1].strip()
            result = find_by_tags(tags)
            print("Quotes with tags:")
            for quote in result:
                print(f"- {quote}")
        else:
            print("Invalid command format. Please use name:, tag:, or tags: followed by appropriate value(s).")


# if __name__ == '__main__':
#     # print(find_by_tag("mi"))
#     # print(find_by_tag("mi"))
#     #
#     # print(find_by_author("Ei"))
#     # print(find_by_author("Ei"))
#
#     # quotes = Quote.objects().all()
#     # print([e.to_mongo().to_dict() for e in quotes])
#
#     quotes = Quote.objects().all()
#     print([e.to_json() for e in quotes])