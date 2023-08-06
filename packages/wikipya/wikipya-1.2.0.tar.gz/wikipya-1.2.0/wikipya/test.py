import asyncio
from aiowiki import Wikipya


async def main():
    w = Wikipya("ru")
    s = await w.search("канобу")
    # s = await w.opensearch("Кот")
    p = await w.getPage(s[0][0])
    print(w.parsePage(p))


if __name__ == "__main__":
    asyncio.run(main())
