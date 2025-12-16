<div id="_desktop_user_info">
  <div class="user-info-container">
    {if $logged}
      {* --- Если клиент авторизован (Личный кабинет и Выход) --- *}
      <a class="auth-link account-link" href="{$my_account_url}" title="{l s='View my customer account' d='Shop.Theme.Customeraccount'}" rel="nofollow">
        <span class="auth-text">{$customerName}</span>
      </a>
      <a class="auth-link logout-link" href="{$logout_url}" rel="nofollow">
        <span class="auth-text">{l s='Wyloguj się' d='Shop.Theme.Actions'}</span>
      </a>
    {else}
      {* --- Если гость (Вход и Регистрация) --- *}
      {* 1. Ссылка на Вход *}
      <a href="{$my_account_url}" class="auth-link login-link" title="{l s='Log in to your customer account' d='Shop.Theme.Customeraccount'}" rel="nofollow">
        <span class="auth-text">{l s='Zaloguj się' d='Shop.Theme.Actions'}</span>
      </a>
      
      {* 2. Ссылка на Регистрацию *}
      <a href="{$urls.pages.register}" class="auth-link register-link" title="{l s='Create an account' d='Shop.Theme.Customeraccount'}" rel="nofollow">
        <span class="auth-text">{l s='Zarejestruj się' d='Shop.Theme.Actions'}</span>
      </a>
    {/if}
  </div>
</div>
