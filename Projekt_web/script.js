// Wenn die Seite geladen wird, werden die Bild-Buttons eingerichtet
window.onload = function() {
    setupImageButtons();
        
    
};
// Funktion, um die Klick-Events für die Bildauswahl-Buttons einzurichten
function setupImageButtons() {
    const image1Url = "https://cdn.pixabay.com/photo/2024/04/09/22/28/trees-8686902_1280.jpg";
    const image2Url = 'https://cdn.pixabay.com/photo/2024/02/20/13/21/mountains-8585535_1280.jpg';
    const image3Url = 'https://cdn.pixabay.com/photo/2024/03/15/17/50/dogs-8635461_1280.jpg';
    const image4Url = 'https://cdn.pixabay.com/photo/2024/03/19/19/08/book-8643905_1280.jpg';

    // Klick-Events für die Bilder zuweisen
    document.getElementById('image1').onclick = function() {
        startPuzzle(image1Url); // Puzzle mit Bild 1 starten
    }
    document.getElementById('image2').onclick = function() {
        startPuzzle(image2Url); // Puzzle mit Bild 2 starten
    }
    document.getElementById('image3').onclick = function() {
        startPuzzle(image3Url); // Puzzle mit Bild 3 starten
    }
    document.getElementById('image4').onclick = function() {
        startPuzzle(image4Url); // Puzzle mit Bild 4 starten
    }
}
// Funktion, um das Puzzle zu starten
function startPuzzle(imageUrl) {
    loadPuzzle(imageUrl); // Puzzle laden
    // Ausblendung der Bildauswahl und der Überschrift
    document.getElementById('image1').style.display = 'none'; 
    document.getElementById('image2').style.display = 'none'; 
    document.getElementById('image3').style.display = 'none'; 
    document.getElementById('image4').style.display = 'none'; 
    document.getElementById('puzzle-start-message').style.display = 'none'; 
    // Drop-Zone für Puzzle anzeigen
    document.getElementById('drop-zone').style.display = 'grid';

    }
// Funktion, um das Puzzle zu laden und die Stücke zu erstellen
function loadPuzzle(imageUrl) {
    const puzzleContainer = document.getElementById('puzzle-container');
    const dropZone = document.getElementById('drop-zone');
    const messageContainer = document.getElementById('message-container'); // Erfolgsnachricht-Container
    // Zurücksetzen des Puzzle-Containers und der Drop-Zone
    puzzleContainer.innerHTML = '';
    dropZone.innerHTML = '';
    messageContainer.innerHTML = ''; // Erfolgsnachricht zurücksetzen

    // Positionen für die Puzzle-Stücke
    const positions = [
        { x: 0, y: 0 }, { x: -60, y: 0 }, { x: -120, y: 0 }, { x: -180, y: 0 }, { x: -240, y: 0 }, 
        { x: 0, y: -60 }, { x: -60, y: -60 }, { x: -120, y: -60 }, { x: -180, y: -60 }, { x: -240, y: -60 }, 
        { x: 0, y: -120 }, { x: -60, y: -120 }, { x: -120, y: -120 }, { x: -180, y: -120 }, { x: -240, y: -120 }, 
        { x: 0, y: -180 }, { x: -60, y: -180 }, { x: -120, y: -180 }, { x: -180, y: -180 }, { x: -240, y: -180 }, 
        { x: 0, y: -240 }, { x: -60, y: -240 }, { x: -120, y: -240 }, { x: -180, y: -240 }, { x: -240, y: -240 }
    ];
    

    // Logge die ursprünglichen Positionen
    console.log("Original positions:", positions);

    const img = new Image(); // Neues Bild-Objekt erstellen
    img.src = imageUrl; // Bildquelle setzen

    // Wenn das Bild geladen ist, das Puzzle erstellen
    img.onload = function() {
        console.log("Bild erfolgreich geladen:", imageUrl);

        let unsorted_pieces = []; // Array für die unsortierten Puzzle-Stücke
    
        // Für jede Position ein Puzzle-Stück erstellen
        positions.forEach((pos, index) => {
            // Puzzle-Stücke erstellen
            const piece = document.createElement('div'); // Neues Puzzle-Stück
            piece.classList.add('puzzle-piece'); // CSS-Klasse hinzufügen
            piece.setAttribute('draggable', 'true'); // Puzzle-Stück ist ziehbar
            piece.id = 'piece' + (index + 1); // Einzigartige ID
            piece.style.backgroundImage = `url(${imageUrl})`; // Bildquelle
            piece.style.backgroundPosition = `${pos.x}px ${pos.y}px`; // Position des Bildausschnitts
            piece.style.backgroundSize = '300px 300px'; // Bildgröße anpassen
            unsorted_pieces.push(piece); // Puzzle-Stück ins Array hinzufügen

            // Drop-Zone für das jeweilige Puzzle-Stück erstellen
            const dropArea = document.createElement('div');
            dropArea.classList.add('drop-area'); // CSS-Klasse hinzufügen
            dropArea.setAttribute('data-piece', piece.id); // Drop-Zone wird einem bestimmten Puzzle-Stück zugewiesen
            dropZone.appendChild(dropArea); // Drop-Zone dem DOM hinzufügen
        });

         // Funktion, um ein Array zu mischen (Fisher-Yates-Algorithmus)
        function shuffleArray(array) {
            for (let i = array.length - 1; i > 0; i--) {
                const j = Math.floor(Math.random() * (i + 1));
                [array[i], array[j]] = [array[j], array[i]]; // Tausche zwei Elemente
            }
            return array; // Gemischtes Array zurückgeben
        }
        console.log('sortierte Teile:', unsorted_pieces)
        
        puzzlePieces = shuffleArray(unsorted_pieces); // Mische die Puzzle-Stücke

        console.log('unsortierte Teile:', unsorted_pieces)

        unsorted_pieces.forEach(piece => {
            puzzleContainer.appendChild(piece); // Füge die gemischten Puzzle-Stücke dem Container hinzu
        })

        addDragAndDropFunctionality(); // Drag-and-Drop-Funktionalität aktivieren
    };
    // Fehlerbehandlung, wenn das Bild nicht geladen werden kann
    img.onerror = function() {
        console.error("Fehler beim Laden des Bildes:", imageUrl);
        alert("Das Bild konnte nicht geladen werden. Bitte überprüfe die URL.");
    };
}

function addDragAndDropFunctionality() {
    const pieces = document.querySelectorAll('.puzzle-piece');
    const dropAreas = document.querySelectorAll('.drop-area');

    // Überprüfe, ob es sich um ein mobiles Gerät handelt
    const isMobile = 'ontouchstart' in window || navigator.maxTouchPoints > 0;

    if (isMobile) {
        // Mobile Geräte: Touch-Events
        pieces.forEach(piece => {
            piece.addEventListener('touchstart', touchStart); // Unterstützung für Touch
        });

        dropAreas.forEach(area => {
            area.addEventListener('touchmove', touchMove); // Unterstützung für Touch
            area.addEventListener('touchend', touchDrop); // Unterstützung für Touch
        });
    } else {
        // Desktop-Geräte: Drag-and-Drop-Events
        pieces.forEach(piece => {
            piece.addEventListener('dragstart', dragStart);
        });

        dropAreas.forEach(area => {
            area.addEventListener('dragover', dragOver);
            area.addEventListener('drop', drop);
        });
    }
}

// Drag-and-Drop-Handler für Desktop
function dragStart(e) {
    e.dataTransfer.setData('text/plain', e.target.id);
}

// Touch-Handler für Mobile Geräte
let activeTouchPiece = null;
let initialX, initialY; // Die Startposition des Touch-Events speichern

function touchStart(e) {
    e.preventDefault();
    const touch = e.touches[0];
    activeTouchPiece = e.target; // Das aktive Puzzlestück speichern

    // Startposition des Puzzlestücks festhalten (relativ zur Seite)
    initialX = touch.pageX;
    initialY = touch.pageY;

    // Position relativ zur Drop-Zone anpassen (Optional)
    activeTouchPiece.style.position = 'absolute';
    activeTouchPiece.style.zIndex = '1000'; // Auf oberste Ebene bringen
    movePiece(initialX, initialY);
}

function touchMove(e) {
    e.preventDefault(); // Verhindert das Scrollen während des Ziehens
    const touch = e.touches[0];
    movePiece(touch.pageX, touch.pageY); // Teile bewegen basierend auf der Touch-Position
}

function movePiece(x, y) {
    if (activeTouchPiece) {
        activeTouchPiece.style.left = `${x - 30}px`; // 30px offset für zentrierte Bewegung
        activeTouchPiece.style.top = `${y - 30}px`;
    }
}

function touchDrop(e) {
    e.preventDefault();
    const dropArea = document.elementFromPoint(e.changedTouches[0].pageX, e.changedTouches[0].pageY);

    if (dropArea.classList.contains('drop-area') && dropArea.getAttribute('data-piece') === activeTouchPiece.id) {
        dropArea.appendChild(activeTouchPiece); // Puzzlestück in die richtige Drop-Zone verschieben
        activeTouchPiece.style.position = 'static'; // Zurück zur normalen Grid-Position
        activeTouchPiece.style.pointerEvents = 'none'; // Verhindert, dass das Stück bewegt werden kann
        dropArea.style.border = '2px solid #4caf50'; // Grüner Rand für die richtige Drop-Zone
        activeTouchPiece = null; // Leere das aktive Puzzlestück

        // Überprüfen, ob das Puzzle gelöst ist
        checkIfPuzzleSolved();
    } else {
        // Wenn nicht korrekt abgelegt, Puzzlestück zurück zur ursprünglichen Position
        resetPiecePosition();
    }
}

function resetPiecePosition() {
    if (activeTouchPiece) {
        // Setze die Puzzlestücke zurück ins Grid
        activeTouchPiece.style.position = 'static';
        activeTouchPiece.style.pointerEvents = 'auto'; // Ermöglicht das Bewegen des Puzzlestücks erneut
        activeTouchPiece = null;
    }
}


// DragOver-Handler für Desktop
function dragOver(e) {
    e.preventDefault(); // Erlaubt das Ablegen von Elementen
}

// Drop-Handler für Desktop
function drop(e) {
    e.preventDefault();
    const id = e.dataTransfer.getData('text');
    const draggableElement = document.getElementById(id);
    const dropArea = e.target;

    if (dropArea.getAttribute('data-piece') === id) {
        dropArea.appendChild(draggableElement);
        draggableElement.style.cursor = 'default';
        draggableElement.setAttribute('draggable', false);
        dropArea.style.border = '2px solid #4caf50';

        // Überprüfen, ob das Puzzle gelöst ist
        checkIfPuzzleSolved();
    }
}



// Funktion, die das Standardverhalten beim Dragover verhindert
function dragOver(e) {
    e.preventDefault(); // Standardaktion verhindern, um Drop zu erlauben
}
// Funktion, die aufgerufen wird, wenn ein Puzzle-Stück in eine Drop-Zone fällt
function drop(e) {
    e.preventDefault();
    const id = e.dataTransfer.getData('text'); // ID des gezogenen Elements holen
    const draggableElement = document.getElementById(id); // Element anhand der ID holen
    const dropArea = e.target; // Aktuelle Drop-Zone

    // Überprüfen, ob das richtige Puzzle-Stück in die richtige Drop-Zone fällt
    if (dropArea.getAttribute('data-piece') === id) {
        dropArea.appendChild(draggableElement); // Puzzle-Stück in die Drop-Zone einfügen
        draggableElement.style.cursor = 'default'; // Cursor ändern
        draggableElement.setAttribute('draggable', false); // Puzzle-Stück kann nicht mehr gezogen werden
        dropArea.style.border = '2px solid #4caf50'; // Rahmen der Drop-Zone grün färben

        // Überprüfen, ob das Puzzle vollständig gelöst ist
        checkIfPuzzleSolved();
    }
}
// Funktion, die überprüft, ob alle Puzzle-Stücke richtig platziert wurden
function checkIfPuzzleSolved() {
    const dropAreas = document.querySelectorAll('.drop-area');
    let allCorrect = true;

    // Überprüfen, ob jedes Puzzle-Stück in der richtigen Zone ist
    dropAreas.forEach(area => {
        const piece = area.querySelector('.puzzle-piece'); // Alle Drop-Zonen
        if (!piece || piece.id !== area.getAttribute('data-piece')) {
            allCorrect = false;
        }
    });

    // Wenn alle Puzzle-Stücke korrekt platziert sind, Erfolgsnachricht anzeigen
    if (allCorrect) {
        displaySuccessMessage();
    }
}
// Funktion, um die Erfolgsnachricht anzuzeigen, wenn das Puzzle gelöst ist
function displaySuccessMessage() {
    const messageContainer = document.getElementById('message-container');
    messageContainer.innerHTML = "Herzlichen Glückwunsch! Du hast das Puzzle gelöst!";
    messageContainer.style.color = 'green'; // Erfolgsnachricht-Stil
    messageContainer.style.fontSize = '24px';
    messageContainer.style.fontWeight = 'bold';
    messageContainer.style.textAlign = 'center';
    messageContainer.style.marginBottom = '20px';
    document.getElementById('play-again-btn').style.display = 'block'; // "Nochmal spielen"-Button anzeigen
}
// Funktion, um das Spiel zurückzusetzen und neu zu starten
function resetGame() {
    document.getElementById('play-again-btn').style.display = 'none'; // Button ausblenden
    document.getElementById('message-container').style.display = 'none'; // Erfolgsnachricht ausblenden
    document.getElementById('drop-zone').style.display = 'none'; // Drop-Zone ausblenden
    document.getElementById('image1').style.display = 'block'; // Bildauswahl wieder anzeigen
    document.getElementById('image2').style.display = 'block'; // Bildauswahl wieder anzeigen
    document.getElementById('image3').style.display = 'block'; // Bildauswahl wieder anzeigen
    document.getElementById('image4').style.display = 'block'; // Bildauswahl wieder anzeigen
    
    // Überschrift wieder anzeigen
    document.getElementById('puzzle-start-message').style.display = 'block';
    setupImageButtons(); // Bildauswahl-Buttons erneut einrichten
}
