<div id="search_widget" class="search-widget" data-search-controller-url="{$search_controller_url}">
  <form method="get" action="{$search_controller_url}">
    <input type="hidden" name="controller" value="search">
    
    <input type="text" name="s" value="{$search_string}" 
           placeholder="{l s='szukaj w sklepie...' d='Shop.Theme.Catalog'}" 
           aria-label="{l s='Search' d='Shop.Theme.Catalog'}"
           class="my-custom-search-input">
           
    <button type="submit" class="my-custom-search-btn">
      <i class="material-icons search">search</i>
      <span class="hidden-xl-down">{l s='Search' d='Shop.Theme.Catalog'}</span>
    </button>
  </form>
</div>
