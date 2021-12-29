import { useEffect } from 'react';
import { useNavigate, useParams } from 'react-router';
import { setSessionId } from '../backend';

export default function OAuthRedirectPage() {
  const navigate = useNavigate();
  const routeParams = useParams();

  useEffect(() => {
    const searchParams = new URLSearchParams(window.location.search);
    const code = searchParams.get('code');
    const state = searchParams.get('state');

    if (code && state) {
      const params = new URLSearchParams();
      params.set('code', code);
      params.set('state', state);

      fetch(`/api/auth/oauth/${routeParams.provider}?${params}`, {
        method: 'GET',
      })
        .then((res) => res.json())
        .then((body) => {
          const { session_id } = body;
          setSessionId(session_id);
          navigate("/bots", { replace: true });
        });
    }
  }, []);
  return null;
}
