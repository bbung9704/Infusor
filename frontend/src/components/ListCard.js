import '../css/List.css';
import HorizonLine from './HorizonLine';

const dateFormat = (time) => {
    const d = new Date(time);
    const year = d.getFullYear()
    const month = d.getMonth()+1
    const date = d.getDate()
    const hour = d.getHours()
    const minute = d.getMinutes()
    const day = d.getUTCDay()
return year + "년 " + month + "월 " + date + "일 " + hour + "시 " + minute + "분 "  +  '일월화수목금토'.charAt(day)+'요일';
}

const ListCard = (prediction) => {

    return (
        <div className="list-container-box">
            <img className="list-image" src={prediction.predictions.url} />
            <HorizonLine />
            <div className='list-detail'>
                <div className='list-detail-volume'>
                    <div id='list-volume'>{prediction.predictions.volume}</div>
                    <div id='list-unit'>mL</div>
                </div>
                <div id='list-time'>{dateFormat(new Date(prediction.predictions.time))}</div>
            </div>
        </div>
    );
};

export default ListCard;