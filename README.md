Change the input and output in sync-comments.py or sync-comments-full.py to your database path and [your-site]/input/media/files/comments. 

add-comment.py allows you to add comments manually. You can run the script and follow the directions.

Update your theme using an override to add the mastodonId field, and then add mastodon Id for all your pots that have a post. 

Make sure to change the instance and usernames to your own. Mine are left in as "sakurajima.moe" and "navi".

Run sync-comments-full.py first to get all the mastodon json data. The other one is for new blog posts only.

If your theme override is setup and your json data is in the correct folder, Publii will pull the JSON data at build and update the bottom of the page with comments.

You can see an example at https://ranobe.pomnavi.net
