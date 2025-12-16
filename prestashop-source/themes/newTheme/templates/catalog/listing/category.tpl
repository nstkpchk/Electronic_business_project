{extends file='catalog/listing/product-list.tpl'}

{block name='product_list_header'}
    {include file='catalog/_partials/category-header.tpl' listing=$listing category=$category}
{/block}

{* ВАЖНО: Тут мы меняем имя блока на subcategory_list, как нашли в твоем коде *}
{block name='subcategory_list'}
    {* Оставляем пустым, чтобы скрыть список *}
{/block}
