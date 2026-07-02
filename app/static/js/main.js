
(() => {
  const readResponse = async (response) => {
    const contentType = response.headers.get('content-type') || '';
    if (contentType.includes('application/json')) {
      return response.json();
    }
    return {
      success: response.ok,
      message: response.ok ? 'Operation completed.' : `Request failed with status ${response.status}`,
      data: {}
    };
  };

  const showMessage = (message, isError = false) => {
    if (!message) return;
    const alert = document.createElement('div');
    alert.className = `alert alert-${isError ? 'danger' : 'success'} alert-dismissible fade show flash-alert api-flash`;
    alert.setAttribute('role', 'alert');
    alert.innerHTML = `
      ${message}
      <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    const container = document.querySelector('.container.mt-5.pt-3') || document.createElement('div');
    if (!container.parentNode) {
      container.className = 'container mt-5 pt-3';
      document.body.prepend(container);
    }
    container.appendChild(alert);
    window.setTimeout(() => {
      if (document.body.contains(alert)) {
        window.bootstrap?.Alert ? bootstrap.Alert.getOrCreateInstance(alert).close() : alert.remove();
      }
    }, 4500);
  };

  const submitApiForm = async (form) => {
    const endpoint = form.dataset.apiEndpoint;
    const method = form.dataset.apiMethod || form.method || 'POST';
    const formData = new FormData(form);
    const body = Object.fromEntries(formData.entries());

    const response = await fetch(endpoint, {
      method,
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify(body)
    });
    const result = await readResponse(response);
    if (!response.ok || result.success === false) {
      showMessage(result.message || 'Request failed.', true);
      return;
    }
    showMessage(result.message || 'Operation completed.');
    const redirectUrl = result.data?.redirect_url;
    if (redirectUrl) {
      window.location.assign(redirectUrl);
    }
  };

  const callApiButton = async (button) => {
    const endpoint = button.dataset.apiEndpoint;
    const method = button.dataset.apiMethod || 'POST';
    button.disabled = true;
    try {
      const response = await fetch(endpoint, {
        method,
        headers: {
          'Accept': 'application/json'
        }
      });
      const result = await readResponse(response);
      if (!response.ok || result.success === false) {
        showMessage(result.message || 'Request failed.', true);
        return;
      }
      showMessage(result.message || 'Operation completed.');
      window.setTimeout(() => window.location.reload(), 600);
    } finally {
      button.disabled = false;
    }
  };

  document.querySelectorAll('form[data-api-endpoint]').forEach((form) => {
    form.addEventListener('submit', (event) => {
      event.preventDefault();
      submitApiForm(form).catch((error) => showMessage(error.message, true));
    });
  });

  document.querySelectorAll('button[data-api-endpoint]').forEach((button) => {
    button.addEventListener('click', () => {
      callApiButton(button).catch((error) => showMessage(error.message, true));
    });
  });
})();
