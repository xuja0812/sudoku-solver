import SwiftUI
import UIKit

#if os(macOS)
import AppKit
#endif

struct ImagePickerView: View {
    @State private var showImagePicker = false
    @State private var selectedImage: UIImage?
    @State private var solvedBoard: [[Int]]? = nil
    @State private var showSolvedBoard = false

    var body: some View {
        NavigationStack {
            ZStack {
                LinearGradient(gradient: Gradient(colors: [Color.purple.opacity(0.3), Color.blue.opacity(0.2)]), startPoint: .topLeading, endPoint: .bottomTrailing)
                    .ignoresSafeArea()

                VStack(spacing: 28) {
                    VStack(spacing: 6) {
                        Text("Sudoku Solver")
                            .font(.largeTitle)
                            .fontWeight(.bold)
                            .foregroundStyle(.primary)
                        Text("Snap a puzzle and solve instantly")
                            .font(.subheadline)
                            .foregroundColor(.secondary)
                    }

                    ZStack {
                        RoundedRectangle(cornerRadius: 20)
                            .fill(Color.white)
                            .frame(height: 300)
                            .shadow(color: .purple.opacity(0.3), radius: 8, x: 0, y: 4)

                        if let image = selectedImage {
                            Image(uiImage: image)
                                .resizable()
                                .scaledToFit()
                                .frame(height: 280)
                                .cornerRadius(16)
                                .padding()
                        } else {
                            VStack(spacing: 10) {
                                Image(systemName: "camera.viewfinder")
                                    .resizable()
                                    .scaledToFit()
                                    .frame(width: 80, height: 80)
                                    .foregroundColor(.purple)
                                Text("No image selected")
                                    .font(.callout)
                                    .foregroundColor(.gray)
                            }
                        }
                    }
                    .padding(.horizontal)

                    Button(action: {
                        #if os(macOS)
                        let panel = NSOpenPanel()
                        panel.allowedFileTypes = ["png", "jpg", "jpeg"]
                        panel.allowsMultipleSelection = false
                        panel.canChooseDirectories = false
                        if panel.runModal() == .OK, let url = panel.url,
                           let nsImage = NSImage(contentsOf: url),
                           let image = nsImage.toUIImage() {
                            selectedImage = image
                        }
                        #else
                        showImagePicker = true
                        #endif
                    }) {
                        HStack {
                            Image(systemName: "photo.on.rectangle")
                            Text("Select Sudoku Image")
                                .fontWeight(.semibold)
                        }
                        .frame(maxWidth: .infinity)
                        .padding()
                        .background(LinearGradient(colors: [Color.blue, Color.purple], startPoint: .leading, endPoint: .trailing))
                        .foregroundColor(.white)
                        .cornerRadius(14)
                        .shadow(color: Color.purple.opacity(0.3), radius: 5, x: 0, y: 2)
                    }
                    .padding(.horizontal)

                    if selectedImage != nil {
                        Button(action: {
                            if let image = selectedImage {
                                sendSudokuImage(image) { board in
                                    if let board = board {
                                        DispatchQueue.main.async {
                                            self.solvedBoard = board
                                            self.showSolvedBoard = true
                                        }
                                    }
                                }
                            }
                        }) {
                            Text("Solve Sudoku")
                                .fontWeight(.semibold)
                                .frame(maxWidth: .infinity)
                                .padding()
                                .background(LinearGradient(colors: [Color.green, Color.blue], startPoint: .leading, endPoint: .trailing))
                                .foregroundColor(.white)
                                .cornerRadius(14)
                                .shadow(color: Color.purple.opacity(0.3), radius: 5, x: 0, y: 2)
                        }
                        .padding(.horizontal)
                    }
                }
                .padding()
            }
            #if os(iOS)
            .sheet(isPresented: $showImagePicker) {
                UIKitImagePicker { image in
                    self.selectedImage = image
                }
            }
            #endif
            .navigationDestination(isPresented: $showSolvedBoard) {
                if let board = solvedBoard {
                    SolvedBoardView(board: board)
                }
            }
        }
    }
}

#if os(iOS)
struct UIKitImagePicker: UIViewControllerRepresentable {
    @Environment(\.presentationMode) var presentationMode
    var sourceType: UIImagePickerController.SourceType = .photoLibrary
    var onImagePicked: (UIImage) -> Void

    func makeUIViewController(context: Context) -> UIImagePickerController {
        let picker = UIImagePickerController()
        picker.sourceType = sourceType
        picker.delegate = context.coordinator
        return picker
    }

    func updateUIViewController(_ uiViewController: UIImagePickerController, context: Context) {}

    func makeCoordinator() -> Coordinator {
        Coordinator(self)
    }

    class Coordinator: NSObject, UIImagePickerControllerDelegate, UINavigationControllerDelegate {
        let parent: UIKitImagePicker

        init(_ parent: UIKitImagePicker) {
            self.parent = parent
        }

        func imagePickerController(_ picker: UIImagePickerController,
                                   didFinishPickingMediaWithInfo info: [UIImagePickerController.InfoKey : Any]) {
            if let image = info[.originalImage] as? UIImage {
                parent.onImagePicked(image)
            }
            parent.presentationMode.wrappedValue.dismiss()
        }

        func imagePickerControllerDidCancel(_ picker: UIImagePickerController) {
            parent.presentationMode.wrappedValue.dismiss()
        }
    }
}
#endif

#if os(macOS)
extension NSImage {
    func toUIImage() -> UIImage? {
        guard let tiffData = self.tiffRepresentation,
              let bitmap = NSBitmapImageRep(data: tiffData),
              let data = bitmap.representation(using: .jpeg, properties: [:]) else {
            return nil
        }
        return UIImage(data: data)
    }
}
#endif

func sendSudokuImage(_ image: UIImage, completion: @escaping ([[Int]]?) -> Void) {
    guard let url = URL(string: "http://127.0.0.1:8000/solve") else {
        print("Invalid URL")
        return
    }

    var request = URLRequest(url: url)
    request.httpMethod = "POST"

    let boundary = "Boundary-\(UUID().uuidString)"
    request.setValue("multipart/form-data; boundary=\(boundary)", forHTTPHeaderField: "Content-Type")

    var body = Data()
    body.append("--\(boundary)\r\n".data(using: .utf8)!)
    body.append("Content-Disposition: form-data; name=\"file\"; filename=\"sudoku.jpg\"\r\n".data(using: .utf8)!)
    body.append("Content-Type: image/jpeg\r\n\r\n".data(using: .utf8)!)
    body.append(image.jpegData(compressionQuality: 1.0)!)
    body.append("\r\n--\(boundary)--\r\n".data(using: .utf8)!)

    request.httpBody = body

    URLSession.shared.dataTask(with: request) { data, response, error in
        if let error = error {
            print("Error:", error)
            completion(nil)
            return
        }

        guard let data = data else {
            print("No data received")
            completion(nil)
            return
        }

        do {
            if let json = try JSONSerialization.jsonObject(with: data) as? [String: Any],
               let board = json["board"] as? [[Int]] {
                completion(board)
            } else {
                print("Failed to parse JSON")
                completion(nil)
            }
        } catch {
            print("JSON error:", error)
            completion(nil)
        }
    }.resume()
}

// Preview (optional)
#Preview {
    ImagePickerView()
}
