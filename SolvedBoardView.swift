import SwiftUI

struct SolvedBoardView: View {
    let board: [[Int]]
    let cellSize: CGFloat = 36
    let thickLineWidth: CGFloat = 2
    let thinLineWidth: CGFloat = 0.5

    var body: some View {
        VStack(spacing: 16) {
            Text("Solved Board")
                .font(.title)
                .fontWeight(.semibold)

            ZStack {
                VStack(spacing: 0) {
                    ForEach(0..<9, id: \.self) { row in
                        HStack(spacing: 0) {
                            ForEach(0..<9, id: \.self) { col in
                                Text("\(board[row][col])")
                                    .frame(width: cellSize, height: cellSize)
                                    .background(Color.white)
                                    .border(.black.opacity(0.2), width: thinLineWidth)
                                    .overlay(
                                        VStack {
                                            if col == 2 || col == 5 {
                                                Rectangle()
                                                    .frame(width: thickLineWidth)
                                                    .foregroundColor(.black)
                                                    .offset(x: (thickLineWidth / 4), y: 0)
                                            } else {
                                                EmptyView()
                                            }
                                        },
                                        alignment: .trailing
                                    )
                            }
                        }
                        .overlay(
                            Rectangle()
                                .frame(height: (row == 2 || row == 5) ? thickLineWidth : thinLineWidth)
                                .foregroundColor(.black),
                            alignment: .bottom
                        )
                    }
                }
            }
            .background(Color.gray.opacity(0.1))
            .cornerRadius(12)
            .shadow(color: Color.purple.opacity(0.2), radius: 4, x: 0, y: 2)

            Spacer()
        }
        .padding()
        .navigationTitle("Solution")
        .navigationBarTitleDisplayMode(.inline)
    }
}

#Preview {
    SolvedBoardView(board: Array(repeating: [1,2,3,4,5,6,7,8,9], count: 9))
}
