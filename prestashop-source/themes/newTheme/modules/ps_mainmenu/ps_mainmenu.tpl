{assign var=_counter value=0}
{function name="menu" nodes=[] depth=0 parent=null}
    {if $nodes|count}
      {* Если это верхний уровень, даем ID top-menu, если вложенный - просто класс *}
      <ul class="{if $depth == 0}top-menu{else}sub-menu-ul{/if}" {if $depth == 0}id="top-menu"{/if} data-depth="{$depth}">
        
        {foreach from=$nodes item=node}
            {* Класс 'has-children' добавляется, если есть подкатегории *}
            <li class="{$node.type} item-depth-{$depth} {if $node.children|count}has-children{/if}" id="{$node.page_identifier}">
              
              {* Ссылка на категорию *}
              <a href="{$node.url}" data-depth="{$depth}" {if $node.open_in_new_window} target="_blank" {/if}>
                {$node.label}
              </a>

              {* САМОЕ ВАЖНОЕ: Если есть дети, создаем выпадающий блок (popover) *}
              {if $node.children|count}
                <div class="popover sub-menu js-sub-menu collapse">
                  {menu nodes=$node.children depth=$depth+1 parent=$node}
                </div>
              {/if}
              
            </li>
        {/foreach}
      </ul>
    {/if}
{/function}

<div class="menu js-top-menu position-static hidden-sm-down" id="_desktop_top_menu">
    {menu nodes=$menu.children}
    <div class="clearfix"></div>
</div>
