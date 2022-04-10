# ciudadano

## Project setup
```
yarn install
```

### Compiles and hot-reloads for development
```
yarn serve
```

### Compiles and minifies for production
```
yarn build
```

### Lints and fixes files
```
yarn lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).


yarn build
cd dist
aws --profile sectorpublico s3 sync . s3://analyze-chilepaga/prod --acl public-read
aws cloudfront create-invalidation --distribution-id E2316HCAQ13GWT --paths "/*" --profile sectorpublico
cd ..
