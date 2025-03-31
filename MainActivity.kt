package com.example.fantasycricket

import android.os.Bundle import android.widget.Toast import androidx.activity.ComponentActivity import androidx.activity.compose.setContent import androidx.compose.foundation.layout.* import androidx.compose.foundation.lazy.LazyColumn import androidx.compose.foundation.lazy.items import androidx.compose.material3.* import androidx.compose.runtime.* import androidx.compose.ui.Modifier import androidx.compose.ui.unit.dp import okhttp3.* import org.json.JSONArray import java.io.IOException

class MainActivity : ComponentActivity() { override fun onCreate(savedInstanceState: Bundle?) { super.onCreate(savedInstanceState) setContent { FantasyCricketApp() } } }

@Composable fun FantasyCricketApp() { var contestList by remember { mutableStateOf(listOf<String>()) } var isLoading by remember { mutableStateOf(false) }

Column(modifier = Modifier.padding(16.dp)) {
    Button(onClick = {
        isLoading = true
        fetchContests { contests ->
            contestList = contests
            isLoading = false
        }
    }, modifier = Modifier.padding(bottom = 8.dp)) {
        Text("Get Contests")
    }

    if (isLoading) {
        CircularProgressIndicator()
    } else {
        LazyColumn {
            items(contestList) { contest ->
                Text(text = contest, modifier = Modifier.padding(8.dp))
            }
        }
    }
}

}

fun fetchContests(callback: (List<String>) -> Unit) { val client = OkHttpClient() val request = Request.Builder() .url("http://103.124.172.98:5000/contest_details") .build()

client.newCall(request).enqueue(object : Callback {
    override fun onFailure(call: Call, e: IOException) {
        e.printStackTrace()
    }

    override fun onResponse(call: Call, response: Response) {
        response.body?.string()?.let {
            val contests = JSONArray(it).getJSONArray(0)
            val contestList = mutableListOf<String>()
            for (i in 0 until contests.length()) {
                val contest = contests.getJSONArray(i)
                contestList.add("${contest.getString(1)} - Entry Fee: ${contest.getInt(2)}")
            }
            callback(contestList)
        }
    }
})

}

