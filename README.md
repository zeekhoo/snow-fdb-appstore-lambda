# Lambdas for the Snowflake-Fauna AppStore


## Deploying to AWS
1. Create a new Lambda function
   * Runtime = Python 3.9
2. For the source code, **Upload** the `snow-fdb-appstore.zip` file
3. Add an Environment Variable `FAUNADB_SECRET` = `<<fauna key>>`
4. Update the Runtime settings:
   * handler = `handler.handle_event`

## Modifying the script
1. Modify handler.py
2. Test your changes:
  * Set the `FAUNADB_SECRET` environment variable:
    ```
    export FAUNADB_SECRET=<<fauna key>>
    ```
    > Obtain `<<fauna key>>` from the Fauna dashboard
3. Add the updated handler.py to the zip bundle:
   ```
   zip -g snow-fdb-appstore.zip handler.py
   ```


---

## Installing additional modules
Calling Fauna from Python requires the use of the [Python Driver](https://docs.fauna.com/fauna/current/drivers/python).
So we must install it first, then zip it up along with any new modules you need to install.
1. Start virtual env
```
python3 -m venv venv
```
2. Activate virtualenv
```
source venv/bin/activate
```
3. Install requirements
```
pip install -r requirements
```
4. Now install any other modules
5. Edit handler.py with any necessary changes
6. Test your changes
7. zip up the installed modules:
   ```
   cd venv/lib/python3.9/site-packages
   zip -r9 ../../../../snow-fdb-appstore.zip . ../../../../handler.py
   ```
   > The above zips all the files in `site-packages` together with `handler.py` into the zip archive `snow-fdb-appstore.zip`
