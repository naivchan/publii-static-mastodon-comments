This is where you upload these files to your theme override. You need to update take post.hbs and copy the important parts into your theme's post.hbs (or create a [Theme-Name]-override folder and copy the theme's original files there before editing). 

Make sure to add this to your theme override under postConfig:

```JSON
{ 
  "name": "mastodonId",
  "label": "Mastodon Post ID",
  "value": "",
  "type": "text",
  "note": "Enter the numeric ID of the Mastodon post for comments."
}, 
```


This theme override is for Publii's Mercury Theme
