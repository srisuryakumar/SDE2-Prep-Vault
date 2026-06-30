# Chapter 11: LLD Design 7 — Chess Game

> Chess is the ultimate OOP modeling exercise: a deep inheritance hierarchy, complex behavioral polymorphism, and intricate state management all in one problem.

---

## Step 1: Requirements

- 8×8 board, two players (White and Black)
- All pieces with correct movement rules
- Move validation: can't move into check
- Special moves: castling, en passant, pawn promotion
- Game states: ACTIVE, CHECK, CHECKMATE, STALEMATE

---

## Step 2: Class Hierarchy

```
Piece (abstract)
    ├── King
    ├── Queen
    ├── Rook
    ├── Bishop
    ├── Knight
    └── Pawn

Board
    └── Cell[8][8] → Optional<Piece>

Game
    ├── Board
    ├── Player (WHITE / BLACK)
    └── GameStatus (ACTIVE, CHECK, CHECKMATE, STALEMATE)

Move
    ├── from: Position
    ├── to: Position
    └── type: NORMAL, CASTLING, EN_PASSANT, PROMOTION
```

---

## Step 3: Full Java Implementation

```java
// ── Core Types ────────────────────────────────────────────────────────────

public enum PieceColor { WHITE, BLACK }
public enum GameStatus  { ACTIVE, CHECK, CHECKMATE, STALEMATE }
public enum MoveType    { NORMAL, CASTLING, EN_PASSANT, PROMOTION }

public class Position {
    public final int row; // 0-7 (0 = rank 1, 7 = rank 8)
    public final int col; // 0-7 (0 = file a, 7 = file h)

    public Position(int row, int col) {
        this.row = row;
        this.col = col;
    }

    public boolean isValid() {
        return row >= 0 && row < 8 && col >= 0 && col < 8;
    }

    public Position offset(int dRow, int dCol) {
        return new Position(row + dRow, col + dCol);
    }

    @Override
    public boolean equals(Object o) {
        if (!(o instanceof Position)) return false;
        Position p = (Position) o;
        return row == p.row && col == p.col;
    }

    @Override
    public int hashCode() { return row * 8 + col; }

    @Override
    public String toString() {
        return String.format("%c%d", (char)('a' + col), row + 1);
    }
}

public class Move {
    public final Position from;
    public final Position to;
    public final MoveType type;
    public final Piece promotionPiece; // non-null only for PROMOTION

    public Move(Position from, Position to) {
        this(from, to, MoveType.NORMAL, null);
    }

    public Move(Position from, Position to, MoveType type, Piece promotionPiece) {
        this.from           = from;
        this.to             = to;
        this.type           = type;
        this.promotionPiece = promotionPiece;
    }
}
```

```java
// ── Board ─────────────────────────────────────────────────────────────────

public class Board {
    private final Piece[][] grid; // grid[row][col]

    public Board() {
        grid = new Piece[8][8];
    }

    // Deep copy constructor for move simulation
    public Board(Board other) {
        this.grid = new Piece[8][8];
        for (int r = 0; r < 8; r++)
            for (int c = 0; c < 8; c++)
                this.grid[r][c] = other.grid[r][c]; // pieces are immutable-ish, sharing is OK
    }

    public Optional<Piece> getPiece(Position pos) {
        if (!pos.isValid()) return Optional.empty();
        return Optional.ofNullable(grid[pos.row][pos.col]);
    }

    public void setPiece(Position pos, Piece piece) {
        grid[pos.row][pos.col] = piece;
    }

    public void removePiece(Position pos) {
        grid[pos.row][pos.col] = null;
    }

    public void movePiece(Position from, Position to) {
        Piece piece = grid[from.row][from.col];
        grid[to.row][to.col]   = piece;
        grid[from.row][from.col] = null;
        if (piece != null) piece.setPosition(to);
    }

    // Is a given position under attack by any piece of the given color?
    public boolean isUnderAttack(Position pos, PieceColor attackingColor) {
        for (int r = 0; r < 8; r++) {
            for (int c = 0; c < 8; c++) {
                Piece piece = grid[r][c];
                if (piece != null && piece.getColor() == attackingColor) {
                    if (piece.getAttackSquares(this).contains(pos)) {
                        return true;
                    }
                }
            }
        }
        return false;
    }

    public Optional<Position> findKing(PieceColor color) {
        for (int r = 0; r < 8; r++)
            for (int c = 0; c < 8; c++)
                if (grid[r][c] instanceof King && grid[r][c].getColor() == color)
                    return Optional.of(new Position(r, c));
        return Optional.empty();
    }

    public List<Piece> getAllPieces(PieceColor color) {
        List<Piece> pieces = new ArrayList<>();
        for (int r = 0; r < 8; r++)
            for (int c = 0; c < 8; c++)
                if (grid[r][c] != null && grid[r][c].getColor() == color)
                    pieces.add(grid[r][c]);
        return pieces;
    }

    // Initialize standard starting position
    public static Board createStandardBoard() {
        Board board = new Board();
        // White pieces (row 0 and 1)
        board.grid[0][0] = new Rook(PieceColor.WHITE, new Position(0, 0));
        board.grid[0][1] = new Knight(PieceColor.WHITE, new Position(0, 1));
        board.grid[0][2] = new Bishop(PieceColor.WHITE, new Position(0, 2));
        board.grid[0][3] = new Queen(PieceColor.WHITE, new Position(0, 3));
        board.grid[0][4] = new King(PieceColor.WHITE, new Position(0, 4));
        board.grid[0][5] = new Bishop(PieceColor.WHITE, new Position(0, 5));
        board.grid[0][6] = new Knight(PieceColor.WHITE, new Position(0, 6));
        board.grid[0][7] = new Rook(PieceColor.WHITE, new Position(0, 7));
        for (int c = 0; c < 8; c++)
            board.grid[1][c] = new Pawn(PieceColor.WHITE, new Position(1, c));

        // Black pieces (row 7 and 6)
        board.grid[7][0] = new Rook(PieceColor.BLACK, new Position(7, 0));
        board.grid[7][1] = new Knight(PieceColor.BLACK, new Position(7, 1));
        board.grid[7][2] = new Bishop(PieceColor.BLACK, new Position(7, 2));
        board.grid[7][3] = new Queen(PieceColor.BLACK, new Position(7, 3));
        board.grid[7][4] = new King(PieceColor.BLACK, new Position(7, 4));
        board.grid[7][5] = new Bishop(PieceColor.BLACK, new Position(7, 5));
        board.grid[7][6] = new Knight(PieceColor.BLACK, new Position(7, 6));
        board.grid[7][7] = new Rook(PieceColor.BLACK, new Position(7, 7));
        for (int c = 0; c < 8; c++)
            board.grid[6][c] = new Pawn(PieceColor.BLACK, new Position(6, c));

        return board;
    }
}
```

```java
// ── Piece Hierarchy ───────────────────────────────────────────────────────

public abstract class Piece {
    protected PieceColor color;
    protected Position position;
    protected boolean hasMoved; // important for castling, pawn first move

    protected Piece(PieceColor color, Position position) {
        this.color    = color;
        this.position = position;
        this.hasMoved = false;
    }

    public PieceColor getColor()   { return color; }
    public Position getPosition()  { return position; }
    public boolean hasMoved()      { return hasMoved; }

    public void setPosition(Position pos) {
        this.position = pos;
        this.hasMoved = true;
    }

    // Returns positions this piece can move TO (not squares it attacks for capture)
    public abstract List<Position> getValidMoves(Board board);

    // Returns positions this piece can capture/attack (may differ from movement for pawns)
    public List<Position> getAttackSquares(Board board) {
        return getValidMoves(board); // default: attack = move
    }

    // Helper: can this piece move to the given position (not occupied by same color)?
    protected boolean canMoveTo(Position pos, Board board) {
        if (!pos.isValid()) return false;
        Optional<Piece> occupant = board.getPiece(pos);
        return occupant.isEmpty() || occupant.get().getColor() != color;
    }

    // Helper: collect moves along a ray (for Rook, Bishop, Queen)
    protected List<Position> collectRayMoves(Board board, int[] dRows, int[] dCols) {
        List<Position> moves = new ArrayList<>();
        for (int i = 0; i < dRows.length; i++) {
            Position current = position;
            while (true) {
                current = current.offset(dRows[i], dCols[i]);
                if (!current.isValid()) break;
                Optional<Piece> occupant = board.getPiece(current);
                if (occupant.isEmpty()) {
                    moves.add(current);
                } else {
                    if (occupant.get().getColor() != color) moves.add(current); // capture
                    break; // blocked
                }
            }
        }
        return moves;
    }
}

public class King extends Piece {
    public King(PieceColor color, Position position) { super(color, position); }

    @Override
    public List<Position> getValidMoves(Board board) {
        List<Position> moves = new ArrayList<>();
        int[][] offsets = {{1,0},{-1,0},{0,1},{0,-1},{1,1},{1,-1},{-1,1},{-1,-1}};
        for (int[] o : offsets) {
            Position target = position.offset(o[0], o[1]);
            if (canMoveTo(target, board)) moves.add(target);
        }
        return moves;
    }
}

public class Queen extends Piece {
    public Queen(PieceColor color, Position position) { super(color, position); }

    @Override
    public List<Position> getValidMoves(Board board) {
        return collectRayMoves(board,
            new int[]{1,-1,0,0,1,1,-1,-1},
            new int[]{0,0,1,-1,1,-1,1,-1}
        );
    }
}

public class Rook extends Piece {
    public Rook(PieceColor color, Position position) { super(color, position); }

    @Override
    public List<Position> getValidMoves(Board board) {
        return collectRayMoves(board,
            new int[]{1,-1,0,0},
            new int[]{0,0,1,-1}
        );
    }
}

public class Bishop extends Piece {
    public Bishop(PieceColor color, Position position) { super(color, position); }

    @Override
    public List<Position> getValidMoves(Board board) {
        return collectRayMoves(board,
            new int[]{1,1,-1,-1},
            new int[]{1,-1,1,-1}
        );
    }
}

public class Knight extends Piece {
    public Knight(PieceColor color, Position position) { super(color, position); }

    @Override
    public List<Position> getValidMoves(Board board) {
        List<Position> moves = new ArrayList<>();
        int[][] offsets = {{2,1},{2,-1},{-2,1},{-2,-1},{1,2},{1,-2},{-1,2},{-1,-2}};
        for (int[] o : offsets) {
            Position target = position.offset(o[0], o[1]);
            if (canMoveTo(target, board)) moves.add(target);
        }
        return moves;
    }
}

public class Pawn extends Piece {
    public Pawn(PieceColor color, Position position) { super(color, position); }

    private int direction() { return color == PieceColor.WHITE ? 1 : -1; }
    private int startRow()  { return color == PieceColor.WHITE ? 1 : 6; }

    @Override
    public List<Position> getValidMoves(Board board) {
        List<Position> moves = new ArrayList<>();
        int dir = direction();

        // One step forward
        Position oneForward = position.offset(dir, 0);
        if (oneForward.isValid() && board.getPiece(oneForward).isEmpty()) {
            moves.add(oneForward);

            // Two steps forward from starting position
            if (position.row == startRow()) {
                Position twoForward = position.offset(2 * dir, 0);
                if (board.getPiece(twoForward).isEmpty()) moves.add(twoForward);
            }
        }

        // Diagonal captures
        for (int dc : new int[]{-1, 1}) {
            Position diagonal = position.offset(dir, dc);
            if (diagonal.isValid()) {
                Optional<Piece> occupant = board.getPiece(diagonal);
                if (occupant.isPresent() && occupant.get().getColor() != color) {
                    moves.add(diagonal);
                }
            }
        }

        return moves;
    }

    @Override
    public List<Position> getAttackSquares(Board board) {
        // Pawns attack diagonally even without a piece there
        List<Position> attacks = new ArrayList<>();
        int dir = direction();
        for (int dc : new int[]{-1, 1}) {
            Position diagonal = position.offset(dir, dc);
            if (diagonal.isValid()) attacks.add(diagonal);
        }
        return attacks;
    }
}
```

```java
// ── Game Engine ───────────────────────────────────────────────────────────

public class ChessGame {
    private Board board;
    private PieceColor currentTurn;
    private GameStatus status;
    private final List<Move> moveHistory;
    private Position enPassantTarget; // track en passant possibility

    public ChessGame() {
        this.board        = Board.createStandardBoard();
        this.currentTurn  = PieceColor.WHITE;
        this.status       = GameStatus.ACTIVE;
        this.moveHistory  = new ArrayList<>();
    }

    public boolean makeMove(Position from, Position to) {
        if (status != GameStatus.ACTIVE) {
            System.out.println("Game is over: " + status);
            return false;
        }

        Optional<Piece> pieceOpt = board.getPiece(from);
        if (pieceOpt.isEmpty() || pieceOpt.get().getColor() != currentTurn) {
            System.out.println("Invalid: no " + currentTurn + " piece at " + from);
            return false;
        }

        Piece piece = pieceOpt.get();
        List<Position> validMoves = piece.getValidMoves(board);

        if (!validMoves.contains(to)) {
            System.out.println("Invalid move: " + from + " → " + to);
            return false;
        }

        // Validate: after the move, the moving player's king must not be in check
        if (wouldLeaveKingInCheck(from, to, currentTurn)) {
            System.out.println("Invalid: move leaves king in check");
            return false;
        }

        // Execute the move
        board.movePiece(from, to);
        moveHistory.add(new Move(from, to));

        // Handle pawn promotion (auto-queen for simplicity)
        if (piece instanceof Pawn) {
            int promotionRow = currentTurn == PieceColor.WHITE ? 7 : 0;
            if (to.row == promotionRow) {
                board.setPiece(to, new Queen(currentTurn, to));
                System.out.println("👑 Pawn promoted to Queen at " + to);
            }
        }

        // Switch turns
        PieceColor opponent = currentTurn == PieceColor.WHITE ? PieceColor.BLACK : PieceColor.WHITE;
        currentTurn = opponent;

        // Update game status
        updateGameStatus();

        System.out.printf("♟ %s moved %s → %s | Status: %s%n",
            piece.getClass().getSimpleName(), from, to, status);
        return true;
    }

    private boolean wouldLeaveKingInCheck(Position from, Position to, PieceColor color) {
        // Simulate the move on a copy of the board
        Board simBoard = new Board(board);
        simBoard.movePiece(from, to);

        Optional<Position> kingPos = simBoard.findKing(color);
        if (kingPos.isEmpty()) return true; // shouldn't happen

        PieceColor opponent = color == PieceColor.WHITE ? PieceColor.BLACK : PieceColor.WHITE;
        return simBoard.isUnderAttack(kingPos.get(), opponent);
    }

    private void updateGameStatus() {
        PieceColor opponent = currentTurn; // it's now the next player's turn
        Optional<Position> kingPos = board.findKing(opponent);
        if (kingPos.isEmpty()) return;

        PieceColor prev = opponent == PieceColor.WHITE ? PieceColor.BLACK : PieceColor.WHITE;
        boolean inCheck = board.isUnderAttack(kingPos.get(), prev);
        boolean hasLegalMoves = hasAnyLegalMove(opponent);

        if (inCheck && !hasLegalMoves) {
            status = GameStatus.CHECKMATE;
            System.out.println("♚ CHECKMATE! " + prev + " wins!");
        } else if (!inCheck && !hasLegalMoves) {
            status = GameStatus.STALEMATE;
            System.out.println("🤝 STALEMATE! Draw.");
        } else if (inCheck) {
            status = GameStatus.CHECK;
            System.out.println("⚠️ " + opponent + " is in CHECK!");
        } else {
            status = GameStatus.ACTIVE;
        }
    }

    private boolean hasAnyLegalMove(PieceColor color) {
        for (Piece piece : board.getAllPieces(color)) {
            for (Position target : piece.getValidMoves(board)) {
                if (!wouldLeaveKingInCheck(piece.getPosition(), target, color)) {
                    return true;
                }
            }
        }
        return false;
    }

    // Castling validation (simplified)
    public boolean castle(boolean kingSide) {
        int row = currentTurn == PieceColor.WHITE ? 0 : 7;
        Position kingPos  = new Position(row, 4);
        Position rookPos  = kingSide ? new Position(row, 7) : new Position(row, 0);

        Optional<Piece> kingOpt = board.getPiece(kingPos);
        Optional<Piece> rookOpt = board.getPiece(rookPos);

        if (kingOpt.isEmpty() || rookOpt.isEmpty()) return false;
        Piece king = kingOpt.get(); Piece rook = rookOpt.get();

        if (king.hasMoved() || rook.hasMoved()) {
            System.out.println("Cannot castle: King or Rook has moved");
            return false;
        }

        PieceColor opp = currentTurn == PieceColor.WHITE ? PieceColor.BLACK : PieceColor.WHITE;

        // Check squares between are empty and not under attack
        int[] cols = kingSide ? new int[]{5, 6} : new int[]{1, 2, 3};
        for (int c : cols) {
            Position check = new Position(row, c);
            if (board.getPiece(check).isPresent()) { System.out.println("Castle blocked"); return false; }
            if (board.isUnderAttack(check, opp)) { System.out.println("Castle square under attack"); return false; }
        }

        // Execute castling
        int kingTo = kingSide ? 6 : 2;
        int rookTo = kingSide ? 5 : 3;
        board.movePiece(kingPos, new Position(row, kingTo));
        board.movePiece(rookPos, new Position(row, rookTo));
        currentTurn = opp;
        updateGameStatus();
        System.out.println("🏰 " + currentTurn + " castled " + (kingSide ? "king-side" : "queen-side"));
        return true;
    }

    public GameStatus getStatus() { return status; }
    public PieceColor getCurrentTurn() { return currentTurn; }
    public int getMoveCount() { return moveHistory.size(); }
}
```

---

## Interview Questions

**Q: How do you validate that a move doesn't leave the king in check?**

A: Create a copy of the board (`new Board(board)`), apply the move on the copy, find the moving player's king position, and check if any opponent piece attacks that position. If yes, the move is illegal. This simulation approach is clean and correct, though O(P×M) where P = pieces and M = their moves.

**Q: How would you implement en passant?**

A: Track `enPassantTarget` in the `Game`. When a pawn moves two squares, set `enPassantTarget` to the skipped square. On the next turn, if an opposing pawn is adjacent and moves to `enPassantTarget`, remove the captured pawn from the square it currently occupies (one row back from `enPassantTarget`). Clear `enPassantTarget` after any move.

**Q: What design patterns are used in the Chess design?**

A: (1) Composite — Board is a grid of Cells; (2) Template Method — `Piece` defines the move-collection structure, subclasses implement the specifics; (3) Strategy — each `Piece` subclass encapsulates its own movement algorithm; (4) State — GameStatus (ACTIVE, CHECK, CHECKMATE, STALEMATE) drives game behavior.

---

# Chapter 12: LLD Design 8 — Hotel Booking System

---

## Step 1: Requirements

- List hotels by city and date range
- Check room availability for given dates
- Book a room (reserve for date range)
- Prevent double booking with optimistic locking
- Cancellation policy: configurable (free/partial/no refund)
- Pricing: seasonal, weekend, early bird rates
- Review system

---

## Step 2: Full Java Implementation

```java
// ── Entities ──────────────────────────────────────────────────────────────

public enum RoomType   { STANDARD, DELUXE, SUITE, PENTHOUSE }
public enum BookingStatus { PENDING, CONFIRMED, CANCELLED, COMPLETED }

public class Hotel {
    private final String hotelId;
    private final String name;
    private final String city;
    private final int starRating;
    private final List<Room> rooms;

    public Hotel(String hotelId, String name, String city, int starRating) {
        this.hotelId    = hotelId;
        this.name       = name;
        this.city       = city;
        this.starRating = starRating;
        this.rooms      = new ArrayList<>();
    }

    public void addRoom(Room room) { rooms.add(room); }
    public String getHotelId()    { return hotelId; }
    public String getName()       { return name; }
    public String getCity()       { return city; }
    public List<Room> getRooms()  { return Collections.unmodifiableList(rooms); }
}

public class Room {
    private final String roomId;
    private final String roomNumber;
    private final RoomType type;
    private final double basePrice; // per night
    private final Hotel hotel;
    private final int maxOccupancy;

    public Room(String roomId, String roomNumber, RoomType type,
                double basePrice, int maxOccupancy, Hotel hotel) {
        this.roomId      = roomId;
        this.roomNumber  = roomNumber;
        this.type        = type;
        this.basePrice   = basePrice;
        this.maxOccupancy = maxOccupancy;
        this.hotel       = hotel;
    }

    public String getRoomId()     { return roomId; }
    public String getRoomNumber() { return roomNumber; }
    public RoomType getType()     { return type; }
    public double getBasePrice()  { return basePrice; }
    public Hotel getHotel()       { return hotel; }
}

// Tracks availability per room — the booking record
public class RoomBooking {
    private final String bookingId;
    private final Room room;
    private final Guest guest;
    private final LocalDate checkIn;
    private final LocalDate checkOut;
    private BookingStatus status;
    private final double totalPrice;
    private int version; // for optimistic locking

    public RoomBooking(Room room, Guest guest, LocalDate checkIn,
                       LocalDate checkOut, double totalPrice) {
        this.bookingId  = "HBK-" + System.currentTimeMillis();
        this.room       = room;
        this.guest      = guest;
        this.checkIn    = checkIn;
        this.checkOut   = checkOut;
        this.status     = BookingStatus.CONFIRMED;
        this.totalPrice = totalPrice;
        this.version    = 1;
    }

    public boolean overlaps(LocalDate reqCheckIn, LocalDate reqCheckOut) {
        // [checkIn, checkOut) — checkout day room is available again
        return !reqCheckOut.isAfter(checkIn) ? false
             : !reqCheckIn.isBefore(checkOut) ? false
             : true;
    }

    public String getBookingId()    { return bookingId; }
    public Room getRoom()           { return room; }
    public Guest getGuest()         { return guest; }
    public LocalDate getCheckIn()   { return checkIn; }
    public LocalDate getCheckOut()  { return checkOut; }
    public BookingStatus getStatus() { return status; }
    public double getTotalPrice()   { return totalPrice; }
    public int getVersion()         { return version; }

    public void cancel()            { this.status = BookingStatus.CANCELLED; }
    public void incrementVersion()  { this.version++; }
}

public class Guest {
    private final String guestId;
    private final String name;
    private final String email;

    public Guest(String guestId, String name, String email) {
        this.guestId = guestId; this.name = name; this.email = email;
    }

    public String getGuestId() { return guestId; }
    public String getName()    { return name; }
    public String getEmail()   { return email; }
}
```

```java
// ── Pricing Strategy ──────────────────────────────────────────────────────

public interface PricingStrategy {
    double calculateTotalPrice(Room room, LocalDate checkIn, LocalDate checkOut);
}

public class StandardPricingStrategy implements PricingStrategy {
    @Override
    public double calculateTotalPrice(Room room, LocalDate checkIn, LocalDate checkOut) {
        long nights = java.time.temporal.ChronoUnit.DAYS.between(checkIn, checkOut);
        double total = 0;
        LocalDate current = checkIn;
        while (!current.equals(checkOut)) {
            double nightly = room.getBasePrice();
            DayOfWeek day  = current.getDayOfWeek();
            // Weekend premium
            if (day == DayOfWeek.FRIDAY || day == DayOfWeek.SATURDAY) {
                nightly *= 1.3;
            }
            total += nightly;
            current = current.plusDays(1);
        }
        return total;
    }
}

public class EarlyBirdPricingStrategy implements PricingStrategy {
    private final PricingStrategy baseStrategy;
    private static final int EARLY_BIRD_DAYS = 30;
    private static final double DISCOUNT      = 0.15;

    public EarlyBirdPricingStrategy(PricingStrategy baseStrategy) {
        this.baseStrategy = baseStrategy;
    }

    @Override
    public double calculateTotalPrice(Room room, LocalDate checkIn, LocalDate checkOut) {
        double basePrice = baseStrategy.calculateTotalPrice(room, checkIn, checkOut);
        long daysUntilCheckIn = java.time.temporal.ChronoUnit.DAYS.between(LocalDate.now(), checkIn);
        return daysUntilCheckIn >= EARLY_BIRD_DAYS ? basePrice * (1 - DISCOUNT) : basePrice;
    }
}
```

```java
// ── Cancellation Policy ───────────────────────────────────────────────────

public interface CancellationPolicy {
    double calculateRefund(RoomBooking booking);
    String getPolicyName();
}

public class FreeCancellationPolicy implements CancellationPolicy {
    private final int freeCancellationDays; // e.g., 48 hours = 2 days

    public FreeCancellationPolicy(int days) { this.freeCancellationDays = days; }

    @Override
    public double calculateRefund(RoomBooking booking) {
        long daysUntilCheckIn = java.time.temporal.ChronoUnit.DAYS.between(
            LocalDate.now(), booking.getCheckIn());
        return daysUntilCheckIn >= freeCancellationDays ? booking.getTotalPrice() : 0;
    }

    @Override
    public String getPolicyName() { return "FREE_CANCELLATION_" + freeCancellationDays + "D"; }
}

public class PartialRefundPolicy implements CancellationPolicy {
    @Override
    public double calculateRefund(RoomBooking booking) {
        long daysUntilCheckIn = java.time.temporal.ChronoUnit.DAYS.between(
            LocalDate.now(), booking.getCheckIn());
        if (daysUntilCheckIn >= 7)  return booking.getTotalPrice();           // full refund
        if (daysUntilCheckIn >= 2)  return booking.getTotalPrice() * 0.50;   // 50% refund
        return 0;                                                              // no refund
    }

    @Override
    public String getPolicyName() { return "PARTIAL_REFUND"; }
}
```

```java
// ── Hotel Booking Service ─────────────────────────────────────────────────

public class HotelBookingService {
    // In production: database tables with proper indices on (room_id, check_in, check_out)
    private final Map<String, List<RoomBooking>> bookingsByRoom = new ConcurrentHashMap<>();
    private final PricingStrategy pricingStrategy;
    private final CancellationPolicy cancellationPolicy;

    public HotelBookingService(PricingStrategy pricingStrategy,
                                CancellationPolicy cancellationPolicy) {
        this.pricingStrategy    = pricingStrategy;
        this.cancellationPolicy = cancellationPolicy;
    }

    public List<Room> searchAvailableRooms(Hotel hotel, LocalDate checkIn,
                                            LocalDate checkOut, RoomType type) {
        return hotel.getRooms().stream()
            .filter(room -> type == null || room.getType() == type)
            .filter(room -> isRoomAvailable(room, checkIn, checkOut))
            .collect(java.util.stream.Collectors.toList());
    }

    public boolean isRoomAvailable(Room room, LocalDate checkIn, LocalDate checkOut) {
        List<RoomBooking> roomBookings = bookingsByRoom.getOrDefault(
            room.getRoomId(), Collections.emptyList());
        return roomBookings.stream()
            .filter(b -> b.getStatus() == BookingStatus.CONFIRMED)
            .noneMatch(b -> b.overlaps(checkIn, checkOut));
    }

    /**
     * Optimistic locking: we read the booking count, check availability,
     * and write atomically — if another thread booked the same room between
     * our read and write, we retry or fail.
     *
     * In a real DB: UPDATE rooms SET version=version+1 WHERE id=? AND version=?
     * If rows affected = 0, another transaction won → retry.
     */
    public synchronized RoomBooking bookRoom(Room room, Guest guest,
                                              LocalDate checkIn, LocalDate checkOut) {
        // Re-check availability inside synchronized block
        if (!isRoomAvailable(room, checkIn, checkOut)) {
            throw new IllegalStateException(
                "Room " + room.getRoomNumber() + " is not available for the selected dates");
        }

        double price = pricingStrategy.calculateTotalPrice(room, checkIn, checkOut);
        RoomBooking booking = new RoomBooking(room, guest, checkIn, checkOut, price);

        bookingsByRoom
            .computeIfAbsent(room.getRoomId(), k -> new CopyOnWriteArrayList<>())
            .add(booking);

        System.out.printf("✅ Booked: %s %s | %s → %s | ₹%.2f | %s%n",
            room.getHotel().getName(), room.getRoomNumber(),
            checkIn, checkOut, price, guest.getName());
        return booking;
    }

    public double cancelBooking(String bookingId) {
        for (List<RoomBooking> bookings : bookingsByRoom.values()) {
            for (RoomBooking booking : bookings) {
                if (booking.getBookingId().equals(bookingId)
                        && booking.getStatus() == BookingStatus.CONFIRMED) {
                    double refund = cancellationPolicy.calculateRefund(booking);
                    booking.cancel();
                    System.out.printf("❌ Cancelled booking %s | Refund: ₹%.2f%n",
                        bookingId, refund);
                    return refund;
                }
            }
        }
        throw new IllegalArgumentException("Booking not found or already cancelled: " + bookingId);
    }
}
```

---

## Interview Questions

**Q: How do you prevent two guests from booking the same room for overlapping dates?**

A: The `bookRoom` method is `synchronized`. Inside it, we re-check availability (the "double-checked" pattern for booking). For database-backed systems, use pessimistic locking (`SELECT ... FOR UPDATE`) during the availability check, or optimistic locking with a `version` column: the update fails if `version` changed since we read it.

**Q: How does optimistic locking work in practice?**

A: Read the resource with its `version`. Write with a conditional update: `UPDATE bookings SET status='CONFIRMED', version=version+1 WHERE room_id=? AND date_range=? AND version=?`. If `rowsAffected == 0`, another transaction modified it first. Retry or show an error to the user.

Here is the complete `@Version` implementation for the Hotel Booking system:

```java
// ─── Hotel Booking LLD — Optimistic Locking for Room Availability ─────────────

// The core concurrency challenge:
// Two users booking the last available room simultaneously.
// Both check availability (available=true), both try to book.
// Without locking: double booking occurs.

// ── Entity Design ──────────────────────────────────────────────────────────

@Entity
@Table(name = "room_availability",
       indexes = @Index(columnList = "room_id, date", unique = true))
public class RoomAvailability {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private Long roomId;

    @Column(nullable = false)
    private LocalDate date;

    @Column(nullable = false)
    private boolean available = true;

    @Version                        // JPA manages this — auto-incremented on every UPDATE
    @Column(nullable = false)
    private Long version;

    // Getters, setters, constructors
}

@Entity
@Table(name = "hotel_bookings")
public class HotelBooking {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private Long roomId;

    @Column(nullable = false)
    private Long guestId;

    @Column(nullable = false)
    private LocalDate checkIn;

    @Column(nullable = false)
    private LocalDate checkOut;

    @Column(nullable = false)
    private String confirmationCode;

    @Column(nullable = false)
    private LocalDateTime bookedAt;
}

// ── Repository ─────────────────────────────────────────────────────────────

@Repository
public interface RoomAvailabilityRepository extends JpaRepository<RoomAvailability, Long> {

    @Lock(LockModeType.OPTIMISTIC)   // explicit optimistic lock at repository level
    List<RoomAvailability> findByRoomIdAndDateBetweenAndAvailableTrue(
        Long roomId, LocalDate checkIn, LocalDate checkOut);
}

// ── Service with @Version Optimistic Locking ─────────────────────────────────

@Service
@Slf4j
public class HotelBookingService {

    @Autowired private RoomAvailabilityRepository availabilityRepo;
    @Autowired private HotelBookingRepository bookingRepo;

    @Transactional
    public HotelBooking bookRoom(BookingRequest request) {
        // Step 1: Fetch availability for all dates in the booking range
        // The @Version field is loaded with each row
        List<RoomAvailability> slots = availabilityRepo
            .findByRoomIdAndDateBetweenAndAvailableTrue(
                request.getRoomId(),
                request.getCheckIn(),
                request.getCheckOut().minusDays(1)  // exclusive end
            );

        // Step 2: Validate all dates are available
        long expectedDays = ChronoUnit.DAYS.between(request.getCheckIn(), request.getCheckOut());
        if (slots.size() < expectedDays) {
            throw new RoomNotAvailableException(
                "Room " + request.getRoomId() + " is not fully available for the selected dates");
        }

        // Step 3: Mark each availability slot as booked
        // If another transaction modified ANY slot since we loaded it,
        // @Version mismatch → JPA throws ObjectOptimisticLockingFailureException
        // → our transaction rolls back → no double booking
        slots.forEach(slot -> {
            slot.setAvailable(false);
            // @Version is checked in: UPDATE room_availability
            //   SET available=false, version=version+1
            //   WHERE id=? AND version=?    ← if version changed, 0 rows updated → exception
        });
        availabilityRepo.saveAll(slots);  // throws on version mismatch

        // Step 4: Create the confirmed booking record
        HotelBooking booking = new HotelBooking();
        booking.setRoomId(request.getRoomId());
        booking.setGuestId(request.getGuestId());
        booking.setCheckIn(request.getCheckIn());
        booking.setCheckOut(request.getCheckOut());
        booking.setConfirmationCode(generateConfirmationCode());
        booking.setBookedAt(LocalDateTime.now());

        log.info("Room {} booked for guest {} from {} to {}",
            request.getRoomId(), request.getGuestId(),
            request.getCheckIn(), request.getCheckOut());

        return bookingRepo.save(booking);
    }

    private String generateConfirmationCode() {
        return "BK" + System.currentTimeMillis();
    }
}

// ── Exception Handler ──────────────────────────────────────────────────────

@RestControllerAdvice
public class HotelExceptionHandler {

    @ExceptionHandler({
        ObjectOptimisticLockingFailureException.class,
        OptimisticLockException.class
    })
    public ResponseEntity<ErrorResponse> handleOptimisticLock(Exception ex) {
        log.warn("Optimistic lock conflict during hotel booking: {}", ex.getMessage());
        return ResponseEntity
            .status(HttpStatus.CONFLICT)          // 409
            .body(new ErrorResponse(
                "BOOKING_CONFLICT",
                "This room was just booked by another guest. Please select different dates."));
    }

    @ExceptionHandler(RoomNotAvailableException.class)
    public ResponseEntity<ErrorResponse> handleRoomNotAvailable(RoomNotAvailableException ex) {
        return ResponseEntity
            .status(HttpStatus.UNPROCESSABLE_ENTITY)  // 422
            .body(new ErrorResponse("ROOM_NOT_AVAILABLE", ex.getMessage()));
    }
}

// ── Concurrency Test — Proves the Locking Works ─────────────────────────────

@SpringBootTest
@Transactional(propagation = Propagation.NOT_SUPPORTED)  // each thread manages its own tx
class HotelBookingConcurrencyTest {

    @Autowired private HotelBookingService bookingService;
    @Autowired private RoomAvailabilityRepository availabilityRepo;

    @Test
    @DisplayName("When two guests simultaneously book the last available room, only one succeeds")
    void givenOneAvailableRoom_whenTwoGuestsBookSimultaneously_thenOnlyOneSucceeds()
            throws InterruptedException {

        // Arrange: set up one room available for one night
        Long roomId = 1L;
        LocalDate checkIn = LocalDate.now().plusDays(30);
        LocalDate checkOut = checkIn.plusDays(1);

        RoomAvailability slot = new RoomAvailability();
        slot.setRoomId(roomId);
        slot.setDate(checkIn);
        slot.setAvailable(true);
        availabilityRepo.save(slot);

        BookingRequest request = new BookingRequest(roomId, checkIn, checkOut);

        // Act: two guests try to book the SAME room at the SAME instant
        CountDownLatch startLatch = new CountDownLatch(1);  // holds both threads until released
        CountDownLatch finishLatch = new CountDownLatch(2); // waits for both threads to finish

        AtomicInteger successCount = new AtomicInteger(0);
        AtomicInteger conflictCount = new AtomicInteger(0);
        List<String> bookingCodes = Collections.synchronizedList(new ArrayList<>());

        Runnable bookingTask = () -> {
            try {
                startLatch.await();  // both threads wait here until we release simultaneously
                BookingRequest guestRequest = new BookingRequest(roomId, checkIn, checkOut);
                guestRequest.setGuestId(Thread.currentThread().getId()); // unique guest per thread
                HotelBooking booking = bookingService.bookRoom(guestRequest);
                successCount.incrementAndGet();
                bookingCodes.add(booking.getConfirmationCode());
            } catch (ObjectOptimisticLockingFailureException | RoomNotAvailableException e) {
                conflictCount.incrementAndGet(); // expected for one of the two threads
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            } finally {
                finishLatch.countDown();
            }
        };

        Thread guest1 = new Thread(bookingTask, "Guest-1");
        Thread guest2 = new Thread(bookingTask, "Guest-2");
        guest1.start();
        guest2.start();

        startLatch.countDown();     // release BOTH threads simultaneously
        finishLatch.await(10, TimeUnit.SECONDS);  // wait for both to complete

        // Assert: exactly one booking succeeded, exactly one got a conflict error
        assertThat(successCount.get())
            .as("Exactly one guest should successfully book the room")
            .isEqualTo(1);

        assertThat(conflictCount.get())
            .as("Exactly one guest should receive a conflict error")
            .isEqualTo(1);

        assertThat(bookingCodes)
            .as("There should be exactly one confirmation code")
            .hasSize(1);

        // Verify the room is now unavailable
        List<RoomAvailability> slots = availabilityRepo
            .findByRoomIdAndDateBetweenAndAvailableTrue(roomId, checkIn, checkOut.minusDays(1));
        assertThat(slots)
            .as("The room should no longer be available")
            .isEmpty();
    }
}
```

**Q: How would you implement the availability calendar display?**

A: For each room, maintain a sorted list of confirmed bookings. To check a date range: find any overlapping booking with a sweep. Cache the availability in Redis as a bitset per room per month (1 = occupied, 0 = free), invalidating on every booking/cancellation. The calendar display reads from Redis for fast response.

**Q: How do you handle seasonal pricing dynamically?**

A: The `StandardPricingStrategy` iterates day by day and applies multipliers. Add a `PricingRule` table in the DB: each rule has a date range, day-of-week mask, and multiplier. The strategy queries rules and applies the highest-priority match for each night. This makes pricing changes a data operation, not a code change.
