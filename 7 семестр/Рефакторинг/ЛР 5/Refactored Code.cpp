#include <iostream>
#include <string>

using namespace std;

// Объект музыкального трека
class MusicTrack {
private:
	string author;		// автор
    string title;		// название
public:
    MusicTrack(const string& title, const string& author)
        : title(title), author(author) {}

    string getTitle() { return title; }
    string getAuthor() { return author; }
};

// Интерфейс устройства воспроизведения музыки
class AudioPlayer { 
public: 
    virtual void play(MusicTrack track) = 0; 
    virtual ~AudioPlayer() = default; 
}; 

// Проигрыватель музыки
class MediaPlayer : public AudioPlayer {
public: 
    void play(MusicTrack track) {
    	cout << "MediaPlayer plays: "; 
		cout << track.getAuthor() << " - " << track.getTitle() << "\n\n";
	}
};

// Старый плеер с несовместимым интерфейсом
class SoundDevice { 
public: 
    void startPlayback(const string& trackName) { 
        cout << "~~~ " << trackName << " ~~~" << endl;
		cout << "~~~ playback finished ~~~" << "\n\n";
    } 
}; 

// Адаптер: подгоняет SoundDevice под AudioPlayer 
class LegacyPlayer : public AudioPlayer, private SoundDevice { 
public: 
    void play(MusicTrack track) { 
        string trackname = track.getAuthor() + " - " + track.getTitle();
        startPlayback(trackname); 
    } 
};

int main() { 
	MusicTrack track("Despacito", "Luis Fonsi");
	
    AudioPlayer* player = new MediaPlayer(); 
    player->play(track);

	AudioPlayer* oldPlayer = new LegacyPlayer(); 
    oldPlayer->play(track);
    
    delete player; 
    delete oldPlayer; 
    
    return 0; 
}