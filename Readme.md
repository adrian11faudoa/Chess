# Chess Game <br>

### Phase 1: <br>
Local two-player chess (same device)
Core board + pieces + moves (no AI, no online yet)

✅ 8×8 board
✅ All chess pieces
✅ Turn-based (White / Black)
✅ Move validation (basic rules)

Architecture:
    ChessGame/
    │
    ├── Chess.Core        ← game logic (pure C#)
    │   ├── Board.cs
    │   ├── Piece.cs
    │   ├── Game.cs
    │
    ├── Chess.MAUI        ← UI (.NET MAUI)
    │   └── MainPage.xaml
    │
    └── Chess.Console     ← PC version (optional)
    
chess.py 

chess.html

Features included:

Full chess rules — legal move validation, check detection, checkmate & stalemate
Castling (kingside and queenside)
En passant captures
Pawn promotion (auto-promotes to queen)
Unicode chess pieces with colored squares in the terminal
Interactive square selection — type a square like e2 to select, then the destination like e4 to move
Green highlights for valid moves, yellow for the selected piece
Move history display

How to play:

Type a square (e.g. e2) to select your piece — valid destinations light up in green
Type the destination square (e.g. e4) to move
Re-enter the same square to deselect
Type quit to exit
