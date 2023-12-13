# ... (previous code remains the same)

class RumbotApp(QMainWindow):
    def __init__(self):
        # ... (previous code remains the same)

    async def start_viewbotting(self, session, channel_id, num_viewers):
        try:
            url = f"https://wn0.rumble.com/service.php?video_id={channel_id}&name=video.watching-now"
            response = await session.get(url)
            if "data" not in response.json():
                self.show_status_message("Channel doesn't exist.", "red")
                return

            url = "https://wn0.rumble.com/service.php?name=video.watching-now"
            tasks = []
            for _ in range(num_viewers):
                viewer_id = self.generate_viewer_id()
                data = {"video_id": channel_id, "viewer_id": viewer_id}
                task = session.post(url, data=data)
                tasks.append(task)

            await asyncio.gather(*tasks)
            self.enable_ui_elements(False)
        except Exception as e:
            self.show_status_message(f"Error: {str(e)}", "red")

    def on_send_clicked(self):
        channel_id = self.channel_id_entry.text()
        num_viewers = self.num_viewers_entry.text()

        if not channel_id or not num_viewers:
            self.show_status_message("Please enter both fields.", "red")
            return

        num_viewers = int(num_viewers)
        self.show_status_message("Viewers sent...", "green")
        session = httpx.AsyncClient()
        asyncio.create_task(self.start_viewbotting(session, channel_id, num_viewers))

    # ... (other methods remain the same)

if __name__ == "__main__":
    app = QApplication([])
    mainWin = RumbotApp()
    mainWin.show()
    app.exec()
