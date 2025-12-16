<section class="featured-products clearfix">
  
  {* Ваш новый заголовок с классом для серой линии *}
  <h2 class="h2 products-section-title text-uppercase">
    Polecane produkty dla koszykarza i nie tylko
  </h2>

  <div class="products">
    {foreach from=$products item="product"}
      {include file="catalog/_partials/miniatures/product.tpl" product=$product}
    {/foreach}
  </div>

  <a class="all-product-link float-xs-left float-md-right h4" href="{$allProductsLink}">
    {l s='All products' d='Modules.Featuredproducts.Shop'} <i class="material-icons">&#xE315;</i>
  </a>
</section>
