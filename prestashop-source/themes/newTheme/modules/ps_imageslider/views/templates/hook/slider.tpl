{if $homeslider.slides}
	<div class="container">
	      <div class="slider-header-custom">
	          Super oferta
	      </div>
	  </div>

  <div id="carousel" data-ride="carousel" class="carousel slide" data-interval="{$homeslider.speed}" data-wrap="{(string)$homeslider.wrap}" data-pause="{$homeslider.pause}" data-touch="true">
    <ol class="carousel-indicators">
      {foreach from=$homeslider.slides item=slide key=idx}
        <li data-target="#carousel" data-slide-to="{$idx}" class="{if $idx == 0}active{/if}"></li>
      {/foreach}
    </ol>
    <ul class="carousel-inner" role="listbox">
      {foreach from=$homeslider.slides item=slide name='homeslider'}
        <li class="carousel-item {if $smarty.foreach.homeslider.first}active{/if}" role="option" aria-hidden="{if $smarty.foreach.homeslider.first}false{/if}true">
          
          {* --- ВОТ ЗДЕСЬ ИЗМЕНЕНИЕ --- *}
          {* Оборачиваем ваш контент в контейнер, чтобы ограничить ширину *}
          <div class="container">
              <div class="custom-slider-wrapper">
                  {$slide.description nofilter}
              </div>
          </div>
          {* --- КОНЕЦ ИЗМЕНЕНИЯ --- *}

        </li>
      {/foreach}
    </ul>
    
    <div class="direction" aria-label="{l s='Carousel buttons' d='Shop.Theme.Global'}">
      <a class="left carousel-control" href="#carousel" role="button" data-slide="prev">
        <span class="icon-prev hidden-xs" aria-hidden="true">
          <i class="material-icons">&#xE5CB;</i>
        </span>
      </a>
      <a class="right carousel-control" href="#carousel" role="button" data-slide="next">
        <span class="icon-next hidden-xs" aria-hidden="true">
          <i class="material-icons">&#xE5CC;</i>
        </span>
      </a>
    </div>
  </div>
{/if}
