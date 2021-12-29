export function authenticatedSWRFetcher(url: string, requestInit: RequestInit = {}) {
  return authenticatedFetch(url, requestInit).then(res => {
    if (!res.ok) {
      throw new Error("Fetch failed");
    }

    return res.json();
  });
}

export function authenticatedFetch(url: string, requestInit: RequestInit = {}) {
  const session = getSessionId();

  return fetch(url, {
    ...requestInit,
    headers: {
      ...(session ? { Authorization: `Bearer ${session}` } : {}),
      ...(requestInit.headers || {}),
    },
  });
}

function getSessionId() {
  return localStorage.getItem("session_id");
}

export function setSessionId(session_id: string) {
  return localStorage.setItem("session_id", session_id);
}

export function isLoggedIn() {
  return !!getSessionId();
}
