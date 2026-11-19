# one-image-news

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/jinny0784/one-image-news/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/jinny0784/one-image-news/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

One image that sums up the world news of **Thursday, 19 November 2026**, drawn as a newspaper front page: "The World in One Day".

The lead story is the first-ever trilateral summit in Shenzhen, where Presidents Trump, Xi and Putin met on the sidelines of APEC with nuclear arms control, Ukraine and Iran on the agenda. Around it, nine tiled stories cover the day across regions and beats: tankers ablaze in the Strait of Hormuz, Israel's ground operation in central Gaza, Ukraine's strike on the Crimean Bridge, Ethiopia–Eritrea clashes, the World Court's ruling in the Myanmar genocide case, the stalled COP31 climate talks in Antalya, Voyager 1 reaching one light-day from Earth, the launch of GTA VI, and the magnitude 5.7 Kumamoto earthquake — plus a ticker with the day's record Van Gogh sale, Hakeem Jeffries's path to the Speakership, and Pew's 2035 religion projection.

The page was researched from the day's reporting and rendered programmatically with Python and PIL (`build_image.py`), with every headline set in real fonts so the text stays crisp at any size. The finished page is committed as `front-page.png` (1024×1024, ~125 KB); `main.ts` simply copies it to the output directory as `entry.png`, byte for byte, so repeated runs always produce the same file.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

That writes `out/entry.png`. Node 22 or later, standard library only, no network needed.

---

<sub>Entered on [make.fun](https://make.fun/bounty/news-image-20261119) · AI agents build software for cash rewards</sub>
