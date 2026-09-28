import os
import httpx
from dotenv import load_dotenv
from supabase import create_client, Client, ClientOptions

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


# Shared timeout policy for every HTTP call the SDK makes.
# Kenya -> Supabase (US/EU) round trips can be slow; be generous.
_HTTP_TIMEOUT = httpx.Timeout(
    connect=15.0,
    read=60.0,
    write=30.0,
    pool=15.0,
)


def get_client() -> Client:
    """
    Returns a fresh Supabase client using the anon key.

    Store the returned client in st.session_state so it persists
    across reruns, and call set_user_session() on it after login
    so row-level security applies to the logged-in user.
    """
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise RuntimeError(
            "Missing SUPABASE_URL or SUPABASE_KEY. Copy .env.example to .env "
            "and fill in your project values."
        )

    options = ClientOptions(
        postgrest_client_timeout=60,
        storage_client_timeout=60,
    )

    client = create_client(SUPABASE_URL, SUPABASE_KEY, options=options)

    # Patch the auth client's timeout separately. The Supabase SDK
    # creates its own httpx client internally for auth calls, and it
    # is not affected by ClientOptions above.
    try:
        client.auth._client.timeout = _HTTP_TIMEOUT
    except Exception:
        # If the SDK changes its internal structure in a future version,
        # don't crash — just fall back to the SDK's defaults.
        pass

    return client


def set_user_session(client: Client, access_token: str, refresh_token: str) -> None:
    """
    Attaches a logged-in user's session to the client so that
    subsequent table() calls are made as that user and respect
    the RLS policies defined in schema.sql.
    """
    client.auth.set_session(access_token, refresh_token)