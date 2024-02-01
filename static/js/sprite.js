function updateMonsterSprite() {
    var selectedMonster = document.getElementById("monsterDropdown").value;
    var spriteUrl = `https://happytavern.co/.pictures/dwm/monster/${selectedMonster}.png`;
    
    var iframe = document.getElementById("monsterSpriteIframe");
    iframe.src = "about:blank"; // Clear the iframe content
    
    var content = `<style>
                        body {
                            margin: 0;
                            display: flex;
                            justify-content: center;
                            align-items: center;
                            height: 100vh;
                        }

                        img {
                            max-width: 100%;
                            max-height: 100%;
                            object-fit: contain;
                        }
                    </style>
                    <body>
                        <img src="${spriteUrl}" alt="Monster Sprite">
                    </body>`;
    
    iframe.contentWindow.document.open();
    iframe.contentWindow.document.write(content);
    iframe.contentWindow.document.close();
}
