def login_user():
    if "user_email" in st.session_state:
        return

    query_params = st.query_params()
    code = query_params.get("code", [None])[0]

    if code:
        import requests

        token_resp = requests.post("https://oauth2.googleapis.com/token", data={
            "code": code,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "redirect_uri": REDIRECT_URI,
            "grant_type": "authorization_code"
        }).json()

        id_token = token_resp.get("id_token")
        access_token = token_resp.get("access_token")

        if id_token and access_token:
            userinfo_resp = requests.get("https://openidconnect.googleapis.com/v1/userinfo", headers={
                "Authorization": f"Bearer {access_token}"
            }).json()
            st.session_state.user_email = userinfo_resp.get("email")

        st.experimental_set_query_params()  # Nettoie les query params

    elif "user_email" not in st.session_state:
        auth_url = "https://accounts.google.com/o/oauth2/v2/auth?" + urlencode({
            "client_id": CLIENT_ID,
            "redirect_uri": REDIRECT_URI,
            "response_type": "code",
            "scope": SCOPE,
            "access_type": "offline",
            "prompt": "consent"
        })
        st.markdown(f"[🔐 Se connecter avec Google]({auth_url})", unsafe_allow_html=True)
        st.stop()
