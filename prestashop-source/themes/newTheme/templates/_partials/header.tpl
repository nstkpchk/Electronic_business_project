
{block name='header_banner'}
  <div class="header-banner">
    {hook h='displayBanner'}
  </div>
{/block}

{block name='header_nav'}
  <nav class="header-nav">
    <div class="container">
      <div class="row">
        <div class="hidden-sm-down">
          <div class="col-md-5 col-xs-12">
            {hook h='displayNav1'}
          </div>
          <div class="col-md-7 right-nav">
              {hook h='displayNav2'}
          </div>
        </div>
        <div class="hidden-md-up text-sm-center mobile">
          <div class="float-xs-left" id="menu-icon">
            <i class="material-icons d-inline">&#xE5D2;</i>
          </div>
          <div class="float-xs-right" id="_mobile_cart"></div>
          <div class="float-xs-right" id="_mobile_user_info"></div>
          <div class="top-logo" id="_mobile_logo"></div>
          <div class="clearfix"></div>
        </div>
      </div>
    </div>
  </nav>
{/block}

{**
 * ПОЛНАЯ ЗАМЕНА СТРУКТУРЫ HEADER.TPL
 * Строим "Крест" по описанию: 2 этажа, левая часть широкая, правая узкая.
 *}

{block name='header_banner'}
  <div class="header-banner">
    {hook h='displayBanner'}
  </div>
{/block}

{block name='header_nav'}
   {/block}

{block name='header_top'}
  <div class="header-top">
    <div class="container"> <div class="row header-row-top align-items-center">
            
            <div class="col-md-10 left-top-quadrant">
                <div class="row align-items-center">
                    <div class="col-md-4" id="_desktop_logo">
                        {if $shop.logo_details}
                            <a href="{$urls.base_url}">
                                <img class="logo img-responsive" src="{$shop.logo_details.src}" alt="{$shop.name}">
                            </a>
                        {/if}
                    </div>
                    <div class="col-md-8">
                        {widget name="ps_searchbar"}
                    </div>
                </div>
            </div>

            <div class="col-md-2 right-top-quadrant">
                <div class="user-auth-links">
                    {if $customer.is_logged}
                        {* --- Если вошел: Имя и Выход --- *}
                        <a href="{$urls.pages.my_account}" class="auth-link account-link" title="Moje konto">
                            <i class="material-icons">person</i> <span>{$customer.firstname}</span>
                        </a>
                        <a href="{$urls.actions.logout}" class="auth-link logout-link" title="Wyloguj się">
                            <span>Wyloguj się</span>
                        </a>
                    {else}
                        {* --- Если гость: Регистрация и Вход (Вертикально) --- *}
                        <a href="{$urls.pages.register}" class="auth-link register-link">
                            <span>ZAREJESTRUJ SIĘ</span>
                        </a>
                        <a href="{$urls.pages.authentication}" class="auth-link login-link">
                            <span>ZALOGUJ SIĘ</span>
                        </a>
                    {/if}
                </div>
            </div>

       </div>

       <div class="row header-row-bottom align-items-center">
            
            <div class="col-md-10 left-bottom-quadrant">
                 {widget name="ps_mainmenu"}
            </div>

            <div class="col-md-2 right-bottom-quadrant">
                 {widget name="ps_shoppingcart"}
            </div>

       </div>

    </div>
  </div>
  
  {hook h='displayNavFullWidth'}
  
{/block}
