import asyncio
from aiowiki import Wikipya


async def main():
    w = Wikipya("ru")
    s = await w.search("Кот")
    s = await w.opensearch("Кот")
    print(s)
    print(s[-1][0])
    p = await w.getPage(s[0][0])
    print(w.parsePage(p))


if __name__ == "__main__":
    asyncio.run(main())
