import os
import b2sdk.v2 as b2

# ---- required secrets (keep these out of source code!) ----
B2_KEY_ID = ""        # your App Key ID
B2_APP_KEY = ""        # your Application Key
B2_BUCKET_NAME = "Newspods"     # your bucket name

# ---- auth ----
info = b2.InMemoryAccountInfo()
api = b2.B2Api(info)
api.authorize_account("production", B2_KEY_ID, B2_APP_KEY)  # 'production' is the realm

# ---- get bucket ----
bucket = api.get_bucket_by_name(B2_BUCKET_NAME)

# ---- upload a local audio file ----
local_path = "audio3.mp3"
# Use a consistent object key (what the user will download)
object_name = "audio/my-audio3.mp3"

# Tell B2 the content type so browsers/players stream it correctly
file_info = {"Content-Type": "audio/mpeg"}

bucket.upload_local_file(
    local_file=local_path,
    file_name=object_name,
    file_infos=file_info
)

print("Uploaded:", object_name)
