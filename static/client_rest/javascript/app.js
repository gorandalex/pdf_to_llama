const requestApi = async (url, options) => {
    const token = localStorage.getItem("accessToken");
    if (!token) {
        document.location.href = '/';
    }

    if (!options.headers) {
        options.headers = new Headers();
    }

    options.headers.set('Authorization', `Bearer ${token}`);

    let response = await fetch(url, options);

    if (response.status !== 401) {
        return response;
    }

    const refreshToken = localStorage.getItem("refreshToken")

    const refreshTokenOptions = {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${refreshToken}`
        }
    };

    refreshTokenResponse = await fetch('/api/auth/refresh_token', refreshTokenOptions);

    if (refreshTokenResponse.status === 401 || refreshTokenResponse.status === 403) {
        document.location.href = '/';
    } else {
        const result = await refreshTokenResponse.json();
        localStorage.setItem("accessToken", result.access_token)
        localStorage.setItem("refreshToken", result.refresh_token)
        options.headers.set('Authorization', `Bearer ${result.access_token}`);
        response = await fetch(url, options);
        return response;
    }
};