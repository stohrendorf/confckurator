## What the...?

Don't f\*ck with configuration pipelines across multiple environments anymore. Use this
instead.

PS: [Have a look at the wiki.](https://github.com/stohrendorf/confckurator/wiki)

### Why should I use this?
Because 69% of all people have a dirty mind.  And because 42% of all statistical numbers
are made up.

### What's the current state of this?
It's not usable at all, as major points (like a fully implemented API, the frontend and the template retrieval) are not
implemented at all.

### Dev Setup

First, grab and set up a node.js environment with `npm`. Then...

```
cd cnfckurator
npm install
```

Now run `${checkout-root}/server/confckurator.py` and go to the printed URL.

You need to `cd ${checkout-root}/client-api && python3 generate.py` and then update the frontend files after modifying
the client api swagger file.

For updating the frontend files, go to `${checkout-root}/confckurator` and run `npm run build`, or
`ng build` if you have installed `@angular/cli` globally.
