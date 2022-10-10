const searchModule = (() => {
  // const BASE_URL = "http://localhost:3000/api/v1/search";
  const BASE_ORIGIN = window.location.origin;
  const BASE_PATH = "/api/v1/search";
  const BASE_URL = BASE_ORIGIN + BASE_PATH;
  return {
    searchUsers: async () => {
      // 検索窓への入力を取得
      const query = document.querySelector("#search").value;
      const res = await fetch(BASE_URL + "?q=" + query);
      const result = await res.json();
      console.dir(result);
      let body = "";
      //
      for (let i = 0; i < result.length; i++) {
        const user = result[i];
        body += `<tr>
                    <td>${user.id}</td>
                    <td>${user.name}</td>
                    <td>${user.profile}</td>
                    <td>${user.date_of_birth}</td>
                    <td>${user.created_at}</td>
                    <td>${user.updated_at}</td>
                  </tr>`;
      }
      document.querySelector("#users-list").innerHTML = body;
    },
  };
})();
