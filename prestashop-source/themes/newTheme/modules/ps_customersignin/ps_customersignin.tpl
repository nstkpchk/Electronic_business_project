<div id="_desktop_user_info">
  <div class="user-info-container">
    {if $logged}
      <a class="account" href="{$my_account_url}" title="{l s='View my customer account' d='Shop.Theme.Customeraccount'}" rel="nofollow">
        <span class="user-name">{$customerName}</span>
      </a>
      <a class="logout" href="{$logout_url}" rel="nofollow">
        {l s='Sign out' d='Shop.Theme.Actions'}
      </a>
    {else}
      <a href="{$urls.pages.register}" title="{l s='Create an account' d='Shop.Theme.Customeraccount'}" class="auth-link register-link" rel="nofollow">
        <span class="auth-text">Zarejestruj się</span>
      </a>

      <a href="{$my_account_url}" title="{l s='Log in to your customer account' d='Shop.Theme.Customeraccount'}" class="auth-link login-link" rel="nofollow">
        <span class="auth-text">Zaloguj się</span>
      </a>
    {/if}
  </div>
</div>
