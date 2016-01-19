# The Voyage of the Blood Meridian

> I thank God, I shall never again visit a slave-country.
> - Charles R. Darwin

> When the lambs is lost in the mountain, he said. They is cry. Sometime come
> the mother. Sometime the wolf.
> - Cormac McCarthy, Blood Meridian

> America make them believe themselves slaves; but I believe this was written, M.
> They retired to their servants in French, and the kid behind him shifted into
> motion. He sought in the markets in Louisiana.
> - Cormac R. McDarwin

While Charles Darwin was travelling the world on the HMS Beagle, the kid of
Cormac McCarthy's *Blood Meridian* was born to the Leonid meteor showers. This
simple Markov chain-based bots posts to Twitter/Tumblr what happens if you mix
*Blood Merdian* and *The Voyage of the Beagle*.

## Requirements
The bot is based on *Python* and requires on some libraries:
* [NLTK](http://www.nltk.org/) & its *Punkt* models
* [Twython](https://github.com/ryanmcgrath/twython) for accessing the Twitter API
* [PyTumblr](https://github.com/tumblr/pytumblr) to access the Tumblr API
* [PyYAML](http://pyyaml.org/wiki/PyYAML) for reading the config file

## Usage
For now the Markov chain is created from scratch for each run (it's rather fast anyhow). You will need to pass
1. The two source text files
2. The length of the output text you want to generate
3. The service you want to post to: "tumblr" or "twitter" for now

The order of the Markov chain is implemented in principle. For now it's not used while invoking the script, as from my experience only order=2 gives "good" results.

## Where's the source material?
For copyright reasons this repository only contains a slightly modified version of Darwin's *The Voyage of the Beagle*. You'll have to get your own txt-version of *Blood Meridian* somehow.

## Yet another Markov bot?
Yep, I was bored and somehow got the crazy idea to mix the two source
materials. I know the bot is written badly and better ones exist. But this mine.
Also: Feel free to improve on the source code.
