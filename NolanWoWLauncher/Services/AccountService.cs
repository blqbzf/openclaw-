using System;
using System.IO;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;

namespace NolanWoWLauncher.Services;

public class AccountService
{
    private readonly HttpClient _httpClient;
    private readonly string _apiUrl = "http://1.14.59.54:8080/api";

    public AccountService()
    {
        _httpClient = new HttpClient
        {
            Timeout = TimeSpan.FromSeconds(30)
        };
    }

    public async Task<(bool success, string message)> Register(string username, string password, string email)
    {
        try
        {
            var data = new
            {
                username,
                password,
                email
            };

            var json = JsonConvert.SerializeObject(data);
            var content = new StringContent(json, Encoding.UTF8, "application/json");

            var response = await _httpClient.PostAsync($"{_apiUrl}/register", content);
            var responseText = await response.Content.ReadAsStringAsync();

            var result = JsonConvert.DeserializeObject<dynamic>(responseText);

            if (result?.success == true)
            {
                return (true, "注册成功！现在可以登录游戏了。");
            }
            else
            {
                var errorMsg = result?.message ?? "注册失败";
                return (false, errorMsg.ToString());
            }
        }
        catch (Exception ex)
        {
            return (false, $"连接服务器失败: {ex.Message}");
        }
    }

    public async Task<bool> CheckUsernameAvailable(string username)
    {
        try
        {
            var response = await _httpClient.GetAsync($"{_apiUrl}/check-username/{username}");
            var responseText = await response.Content.ReadAsStringAsync();
            var result = JsonConvert.DeserializeObject<dynamic>(responseText);
            return result?.available == true;
        }
        catch
        {
            return false;
        }
    }
}
