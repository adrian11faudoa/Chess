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
    