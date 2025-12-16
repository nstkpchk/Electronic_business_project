<div class="footer-container">
  <div class="container">
    <div class="row">
      
      {* 1. Левая часть: Ссылки (Nasza Firma, Twoje Konto, Informacja) *}
      {* Они выводятся модулем Link List и Customer Account, которые мы оставили в хуке *}
      {block name='hook_footer'}
        {hook h='displayFooter'}
      {/block}

      {* 2. Правая часть: ТВОЙ НОВЫЙ БЛОК (Телефон и контакты) *}
      {* col-md-3 - занимает 1/4 ширины. Подстрой, если нужно *}
      <div class="col-md-3 wrapper footer-custom-contact">
        <h3 class="h3 footer-custom-title">SKLEPKOSZYKARSKI.PL</h3>
        <p class="footer-custom-subtitle">Twój specjalista od koszykówki</p>
        
        <div class="footer-phone-block">
            <a href="tel:888900901" class="footer-big-phone">888 900 901</a>
        </div>
        
        <div class="footer-email-block">
            <a href="mailto:kontakt@sklepkoszykarski.pl" class="footer-email-link">kontakt@sklepkoszykarski.pl</a>
        </div>
      </div>
      
    </div>

    {* 3. Нижняя часть: Оранжевая линия и соцсети *}
    <div class="row">
      <div class="col-md-12">
        <div class="footer-orange-line"></div>
      </div>
    </div>

    <div class="row footer-bottom-content">
      {* Левая сторона: Две строки текста *}
      <div class="col-md-6 footer-bottom-text">
        <p>© 2025 SKLEPKOSZYKARSKI.PL</p>
        <p>Wszelkie prawa zastrzeżone.</p>
      </div>

      <div class="col-md-6 footer-socials">
                    {* Facebook *}
                    <a href="#" class="my-social-icon my-fb" target="_blank">
                        <i class="fab fa-facebook-f"></i>  {* <-- Тут пусто внутри, нет слова facebook *}
                    </a>
                    {* Instagram *}
                    <a href="#" class="my-social-icon my-inst" target="_blank">
                        <i class="fab fa-instagram"></i>   {* <-- Тут пусто внутри *}
                    </a>
                    {* YouTube *}
                    <a href="#" class="my-social-icon my-yt" target="_blank">
                        <i class="fab fa-youtube"></i>     {* <-- Тут пусто внутри *}
                    </a>
                  </div>
    </div>
    
  </div>
</div>
