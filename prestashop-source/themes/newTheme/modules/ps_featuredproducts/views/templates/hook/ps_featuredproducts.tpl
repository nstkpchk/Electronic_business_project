<section class="featured-products clearfix">
  
  {* --- ДОБАВЛЯЕМ КОНТЕЙНЕР --- *}
  <div class="container">
      
      {* Заголовок *}
      <h2 class="h2 products-section-title">
        Polecane produkty dla koszykarza i nie tylko
      </h2>

      {* Товары *}
      <div class="products">
        {foreach from=$products item="product"}
          {include file="catalog/_partials/miniatures/product.tpl" product=$product}
        {/foreach}
      </div>

      
      
  </div>
  {* --- ЗАКРЫВАЕМ КОНТЕЙНЕР --- *}

</section>
