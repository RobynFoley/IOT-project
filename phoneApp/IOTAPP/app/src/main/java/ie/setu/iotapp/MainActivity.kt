package ie.setu.iotapp

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.content.IntentFilter
import android.os.Bundle
import android.util.Log
import androidx.appcompat.app.AppCompatActivity
import java.net.HttpURLConnection
import java.net.URL
import kotlin.concurrent.thread
import android.app.KeyguardManager
import android.os.Handler
import android.os.Looper
class MainActivity : AppCompatActivity() {


    fun sendToPi(state: String) {
        thread {
            try {
                Log.d("NETWORK", "Sending: $state")

                val url = URL("http://192.168.223.251:5000/phone?state=$state")
                val conn = url.openConnection() as HttpURLConnection

                conn.requestMethod = "GET"
                conn.connectTimeout = 5000
                conn.readTimeout = 5000

                val code = conn.responseCode
                val response = conn.inputStream.bufferedReader().readText()

                Log.d("NETWORK", "HTTP code: $code")
                Log.d("NETWORK", "Response: $response")

            } catch (e: Exception) {
                Log.e("NETWORK", "FAILED: ${e.message}")
            }
        }
    }
    fun isPhoneUnlocked(context: Context): Boolean {
        val km = context.getSystemService(Context.KEYGUARD_SERVICE) as KeyguardManager
        return !km.isKeyguardLocked
    }


    private val handler = Handler(Looper.getMainLooper())

    private val screenReceiver = object : BroadcastReceiver() {
        override fun onReceive(context: Context?, intent: Intent?) {

            if (intent?.action == Intent.ACTION_SCREEN_ON) {
                Log.d("PHONE_STATE", "Screen ON")

                thread {
                    Thread.sleep(500) // initial delay, now safely off main thread
                    var unlocked = context?.let { isPhoneUnlocked(it) } ?: false
                    while (unlocked) {
                        Log.d("PHONE_STATE", "UNLOCKED")
                        sendToPi("UNLOCKED")
                        Thread.sleep(500)
                        unlocked = context?.let { isPhoneUnlocked(it) } ?: false
                    }
                    Log.d("PHONE_STATE", "Locked, stopping loop")
                }
            }

            if (intent?.action == Intent.ACTION_SCREEN_OFF) {
                Log.d("PHONE_STATE", "Screen OFF")
                sendToPi("LOCKED")
            }
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val filter = IntentFilter().apply {
            addAction(Intent.ACTION_USER_PRESENT)
            addAction(Intent.ACTION_SCREEN_ON)
            addAction(Intent.ACTION_SCREEN_OFF)
        }

        registerReceiver(screenReceiver, filter)
    }

    override fun onDestroy() {
        super.onDestroy()
        unregisterReceiver(screenReceiver)
    }
}